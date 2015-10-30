<!--{layout:default title:Java Concurrent(三)::Lock详解}-->

可以不用去公司上班了，今天就在家继续学习吧。虽然总觉得在家的效率不是很高，但是未来很长一段没工作的时间都要在家闲着了，努力提高效率吧

--------------------------------------

下面开始进入正题，我们来看一下Java中Lock是如何实现的。

###ReentrantLock

重入锁的lock unlock tryLock等一系列操作都是由其内部java.util.concurrent.locks.ReentrantLock.FairSync/java.util.concurrent.locks.ReentrantLock.NonFairSync类对象实现的，它们的继承关系如下：
<pre class="language-sh"><code>FairSync ----\
              \
			   |-- Sync -- AbstractQueuedSynchronizer -- AbstractOwnableSynchronizer 
              /
NonFairSync--/</code>
</pre>

FairSync/NonFairSync分别实现公平锁/非公平锁，它们的父类都是抽象类

ReadWriteRenntrantLock也类似！

#### AbstractOwnableSynchronizer

我们先从最祖先的类看起，AbstractOwnableSynchronizer类里面只维护了一个拥有锁的线程对象

<pre class="language-java line-numbers">
<code>
public abstract class AbstractOwnableSynchronizer implements java.io.Serializable {
	/**
     * The current owner of exclusive mode synchronization.
     */
    private transient Thread exclusiveOwnerThread;
	
	protected final void setExclusiveOwnerThread(Thread thread) {
        exclusiveOwnerThread = thread;
    }
	
	protected final Thread getExclusiveOwnerThread() {
        return exclusiveOwnerThread;
    }
}</code>
</pre>

####AbstractQueuedSynchronizer

AbstractQueuedSynchronizer类维护了一个节点为线程及运行状态的等待队列，大部分获得锁/释放锁的逻辑都在这个类里面，那么我们就好好看看这个类！

首先来看下双向链表的节点

<pre class="language-java line-numbers">
<code>
static final class Node {
	//用于标识节点处于共享还是互斥模式
    static final Node SHARED = new Node();
    static final Node EXCLUSIVE = null;

    //节点内的线程所处状态常量
	//互斥使用(lock)
    static final int CANCELLED =  1;	//取消
    static final int SIGNAL    = -1;	//需要唤醒(unpark)下一个线程(successor)
	//同步用(condition)
    static final int CONDITION = -2;	//线程处于condition等待状态
    static final int PROPAGATE = -3;	//
	/**
     * Status field, taking on only the values:
     *   SIGNAL:     The successor of this node is (or will soon be)
     *               blocked (via park), so the current node must
     *               unpark its successor when it releases or
     *               cancels. To avoid races, acquire methods must
     *               first indicate they need a signal,
     *               then retry the atomic acquire, and then,
     *               on failure, block.
     *   CANCELLED:  This node is cancelled due to timeout or interrupt.
     *               Nodes never leave this state. In particular,
     *               a thread with cancelled node never again blocks.
     *   CONDITION:  This node is currently on a condition queue.
     *               It will not be used as a sync queue node
     *               until transferred, at which time the status
     *               will be set to 0. (Use of this value here has
     *               nothing to do with the other uses of the
     *               field, but simplifies mechanics.)
     *   PROPAGATE:  A releaseShared should be propagated to other
     *               nodes. This is set (for head node only) in
     *               doReleaseShared to ensure propagation
     *               continues, even if other operations have
     *               since intervened.
     *   0:          None of the above
     *
     * The values are arranged numerically to simplify use.
     * Non-negative values mean that a node doesn't need to
     * signal. So, most code doesn't need to check for particular
     * values, just for sign.
     *
     * The field is initialized to 0 for normal sync nodes, and
     * CONDITION for condition nodes.  It is modified using CAS
     * (or when possible, unconditional volatile writes).
    */
    volatile int waitStatus; //线程状态
	//前驱节点
    volatile Node prev;
	//后继节点
    volatile Node next;
	//线程
    volatile Thread thread;
	//处于condition的节点
    Node nextWaiter;

    final boolean isShared() {
        return nextWaiter == SHARED;
    }

    /**
     * 获取前驱节点
     * @return the predecessor of this node
    */
    final Node predecessor() throws NullPointerException {
        Node p = prev;
        if (p == null)
            throw new NullPointerException();
        else
            return p;
    }

    Node() {    // Used to establish initial head or SHARED marker
    }

    Node(Thread thread, Node mode) {     // Used by addWaiter
        this.nextWaiter = mode;
        this.thread = thread;
    }

    Node(Thread thread, int waitStatus) { // Used by Condition
        this.waitStatus = waitStatus;
        this.thread = thread;
    }
}
</code>
</pre>

AbstractQueuedSynchronizer对象会维护head tail；另外还有int state，用来做重入计数，下面让我们来看下是如何维护队列的

1.队列初始状态

初始状态下

<pre class="language-java">
<code>
exclusiveOwnerThread = null;
state = 0; 
head=tail=null;</code>
</pre>

2. 入队操作enq:

enq方法，当head==tail==null时，说明之前没有元素插入，此时会CAS设置head为一个新node，如果成功，直接设置tail=head(将tail也设置成新node),然后循环继续执行插入

如果队列不为空插入，则CAS更新tail为node，CAS成功后设置原来tail.pre为node

3. 出队操作：

没有提供出队列的操作，只提供了一个setHead方法，能直接设置一个node为队列头

使用队列维护线程的大概过程如下：

1. lock时，当线程没有获取锁时，会调用addWaiter进而调用enq方法，将节点Node(thread, waitStatus=0)加入队列尾，

2. 然后acquireQueued阻塞线程，acquireQueued首先当前结点prev是否是head，是的话说明已经是可执行线程了，直接设置当前结点为head，并立即返回

3. 否则会进行有限次数的循环等待前面的线程节点出队列，达到次数后阻塞等待；

4. 释放资源，先tryRelease释放，失败的话会对head调用unparkSuccessor方法，唤醒队列第一个等待的节点，无论下个要获得锁的节点是否已经被park挂起了，这里都使用unpark进行唤醒

acquireQueued代码如下:

<pre class="language-java line-numbers">
<code>
final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
			//循环
            final Node p = node.predecessor();//获取前驱节点
            if (p == head && tryAcquire(arg)) { //前驱节点是head，则此线程可以获得锁
                setHead(node); //更新head
                p.next = null; // help GC
                failed = false;
                return interrupted;
            } 
			//否则循环等待
            if (shouldParkAfterFailedAcquire(p, node) && 
			//shouldParkAfterFailedAcquire方法会修改当前结点状态
			//若当前结点第一次进入循环，那么waitStatus==0,此时会cas修改为SIGNAL， 返回false
			//若当前结点状态为SIGNAL,那么返回true，下面parkAndCheckInterrupt()会挂起当前线程，进行阻塞等待
			//若当前结点状态为CANCELED，表示线程已经取消，则会删除节点，返回false
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } finally {
        if (failed)
		    //若请求锁失败，则取消请求锁操作
            cancelAcquire(node);
    }
}</code>
</pre>
通过上面这段代码，我们可以看出，在冲突低时，使用自选锁，冲突高时，使用阻塞锁

####Sync

最复杂的AbstractQueuedSynchronizer之后，就是Sync及FairSync/NonFairSync类了，这些类主要是对AbstractQueuedSynchronizer做了进一步的封装，最终暴露出acquire/release方法，供ReentrantLock的lock/unlock使用，这里就不详细说明了。



------------

###Unsafe park unpark

sun.msic.Unsafe类是Sun JDK/Openjdk里面负责直接操作底层数据的类，java中的Atomic内的一些列原子操作都是由Unsafe的compareAndSwap来完成的；上面AbstractQueuedSynchronizer内的park/unpark挂起/唤醒线程也是由Unsafe.park/unpark完成的。

park/unpark不像wait/notify那样，必须在synchronized的Object上进行等待/唤醒，spark可以直接挂起当前线程，unpark(thread)则可以直接唤醒当前线程。

可以说Lock就是由更细粒度的操作：Unsafe的CAS和park/unpark封装而来。

下面就是使用Unsafe.park/unpark的测试代码：

<pre class="language-java line-numbers">
<code>
package test;

import java.lang.reflect.Field;
import java.util.Random;

import sun.misc.Unsafe;

public class Test {
	private static  Unsafe _UNSAFE;
	private static Random rand = new Random();
	static {
		try {
			//由于Java安全机制的限制，非BootClassLoader加载的类均不能实例化Unsafe对象
			//所以必须通过反射来获取theUnsafe，进而获取Unsafe类对象
			Field f = Unsafe.class.getDeclaredField("theUnsafe");
			f.setAccessible(true);
			_UNSAFE = (Unsafe)f.get(null);
		} catch (NoSuchFieldException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SecurityException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	private static final Unsafe UNSAFE = _UNSAFE;
	private static final Thread t1 = new Thread(new Runnable(){
		private int count = 0;
		@Override
		public void run() {
			while(true){
				System.out.println("Thread1 running ... "+(this.count++));
				//唤醒t2线程
				UNSAFE.unpark(t2);
				try {
					Thread.sleep(rand.nextInt(1000));
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}	
		}
	});
	
	private static final Thread t2 = new Thread(new Runnable(){
		private int count = 0;
		@Override
		public void run() {
			while(true){
				//阻塞自身线程，等待unpark
				UNSAFE.park(false, 0L);
				System.out.println("Thread2 running ... "+(this.count++));
				try {
					Thread.sleep(rand.nextInt(1000));
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}	
		}
	});
	public static void main(String[] args) throws InterruptedException {
		// TODO Auto-generated method stub
		System.out.println("hello world");
		
//		t1.setDaemon(true);
//		t2.setDaemon(true);
		t1.start();
		t2.start();
		
		t1.join();
		t2.join();
		
	}

}
</code>
</pre>

------------

参考资料:

* [Unsafe](http://ifeve.com/sun-misc-unsafe/)
* [Park/Unpark](http://blog.csdn.net/hengyunabc/article/details/28126139)

-------
相关文章：

* 上一篇:[Java Concurrent(二)::并发集合](../2015-10-27/java_concurrent01.html)