<!--{layout:default title:常见排序算法}-->

最近正在准备找工作，感觉面试过程中好多人喜欢问排序算法（吐槽一下，虽然大部分公司内的代码根本就不会用到这些算法），于是就在这里整理一下，同时也为面试做做准备吧。

之前整理并且用python实现了这些排序算法[[点此下载python版]](../../attachments/2015-10-29/python-sort.zip),今天就用Java实现一遍吧！

![常用排序算法](../../images/2015-10-29/sort.jpg)

###准备工作

首先定义一个Sort接口

<pre class="language-java line-numbers">
<code>
package com.raven.sorts;
/**
 * 排序
 * @author Raven
 *
 */
public interface Sort<T extends Comparable<T>> {
	void sort(T [] arr);
	/**
	 * 可以计算耗时
	 */
	default long sortCost(T [] arr){
		long curr = System.currentTimeMillis();
		sort(arr);
		return System.currentTimeMillis() - curr;
	}
	/**
	 * 交换素组元素
	 * Java8支持接口默认方法
	 */
	default void swap(T [] arr, int i, int j){
		T tmp = arr[i];
		arr[i] = arr[j];
		arr[j] = tmp;
	}
}</code>
</pre>

测试程序：

<pre class="language-java line-numbers">
<code>
import java.util.Random;

import com.raven.sorts.Sort;

public class Main {
	private static final int[] MAX_SIZE = new int[] {10, 100, 1000, 10000, 100000};
	private static final Random rand = new Random();
	private static final Sort<Integer> sort = null;;
	public static void main(String [] args){
		for(int i = 0;i&lt;MAX_SIZE.length;i++){
			Integer [] arr = genArr(MAX_SIZE[i]);
			if(MAX_SIZE[i]<=10){
				printArr(arr);
			}
			long cost = sort.sortCost(arr);
			if(MAX_SIZE[i]<=10){
				printArr(arr);
			}
			System.out.println("Sort "+MAX_SIZE[i]+",Cost time:"+cost+"ms");
		}
	}
	/**
	 * 生成随机数列
	 * @return
	 */
	private static Integer [] genArr(int maxSize){
		Integer [] arr = new Integer[maxSize];
		for(int i = 0;i&lt;arr.length;i++){
			arr[i] = rand.nextInt(maxSize*100&lt;Integer.MAX_VALUE?maxSize*100:Integer.MAX_VALUE);
		}
		return arr;
	}
	/**
	 * 打印数列
	 * @param arr
	 */
	private static void printArr(Integer [] arr){
		for(int i=0;i&lt;arr.length;i++){
			if(i!=0){
				System.out.print(",");
			}
			System.out.print(arr[i]);
		}
		System.out.println();
	}
}</code>
</pre>

我们的接口定义成了模板类，但是在测试的时候为了简便，使用Integer数组，正好Integer实现Comparable接口。准备工作做完了，下面就开始实现Sort接口吧！

###冒泡排序

冒泡排序是最简单的交换排序算法，思路就是从数组最后一个开始，每次都跟前一个比较，比较小的话就与前一个交换；他的时间复杂度为n*(n-1)/2，也就是O(n^2)

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import com.raven.sorts.Sort;

/**
 * 冒泡排序
 * @author Raven
 *
 */
public class BubbleSort<T extends Comparable<T>> implements Sort<T> {
	@Override
	public void sort(T [] arr) {
		for(int i = arr.length - 1;i >= 0  ; i--){
			for(int j = i-1; j >= 0; j--){
				if(arr[i].compareTo(arr[j])<0){
					this.swap(arr, i, j);
				}
			}
		}
	}
}</code>
</pre>

冒泡排序结果：

Sort 10,Cost time:0ms

Sort 100,Cost time:1ms

Sort 1000,Cost time:10ms

Sort 10000,Cost time:297ms

Sort 100000,Cost time:34840ms

###快速排序

快速排序算法(QuickSort)是对冒泡排序的一种改进。由C. A. R. Hoare在1962年提出。它的基本思想是：通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小，然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

快速排序时间复杂度O(nlogn)

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import com.raven.sorts.Sort;

public class QuickSort<T extends Comparable<T>> implements Sort<T> {

	@Override
	public void sort(T[] arr) {
		this.innerQuickSort(arr, 0, arr.length-1);
	}
	
	private void innerQuickSort(T[] arr, int low, int high){
		if(low&lt;high){
			int min = this.partition(arr, low, high);
			//对前半段递归
			this.innerQuickSort(arr, low, min);
			//对后半段递归
			this.innerQuickSort(arr, min+1, high);
		}
		//递归终止
	}
	
	/**
	 * 以arr[low]为key，将arr[low:high]分成两部分，比key小的在前，比key大的在后
	 * @param arr
	 * @param low
	 * @param high
	 * @reurn 返回分界点
	 */
	private int partition(T[] arr, int low, int high){
		//这里选择第一个元素为key，也可以选择最后一个
		//或者任何一个，选第一个(最后一个)下面方便处理
		T key = arr[low];
		T tmp = arr[low];
		while(low<high){
			while(high>low && arr[high].compareTo(key)>=0){//这里包含==情况，否则如果有相同的元素会死循环
				high--;
			}
			//将比key小的元素移到前面
			arr[low] = arr[high];
			while(low&lt;high && arr[low].compareTo(key)<0){
				low++;
			}
			//将比key大的元素移到前面
			arr[high] = arr[low];
		}
		//保存中间key
		arr[low] = tmp;
		return low;
	}
}</code>
</pre>

快速排序的结果是：

Sort 10,Cost time:0ms

Sort 100,Cost time:0ms

Sort 1000,Cost time:1ms

Sort 10000,Cost time:3ms

Sort 100000,Cost time:105ms

可见性能有明显提升

###选择排序

每一趟从待排序的数据元素中选出最小（或最大）的一个元素，顺序放在已排好序的数列的最后，直到全部待排序的数据元素排完。 选择排序是不稳定的排序方法。时间复杂度也是O(n^2)

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import com.raven.sorts.Sort;

/**
 * 选择排序
 * @author Raven
 *
 * @param <T>
 */
public class SelectSort<T extends Comparable<T>> implements Sort<T> {

	@Override
	public void sort(T[] arr) {
		for(int i = 0;i &lt; arr.length-1; i++){
			//将最小的元素放在位置i
			for(int j = i+1 ;j&lt;arr.length;j++){
				//位置i之后至数组最后的元素j依次进行比较
				//如果arr[j]&lt;arr[i],那么将j位置的元素与i位置的交换
				if(arr[i].compareTo(arr[j])>0){
					this.swap(arr, i, j);
				}
			}
		}
	}
}</code>
</pre>

选择排序结果：

Sort 10,Cost time:0ms

Sort 100,Cost time:0ms

Sort 1000,Cost time:10ms

Sort 10000,Cost time:258ms

Sort 100000,Cost time:34806ms


###堆排序

堆排序(Heapsort)是指利用堆积树（堆）这种数据结构所设计的一种排序算法，可以利用数组的特点快速定位指定索引的元素。

若从小到大对序列N排序，那么堆排序的思路就是首先构建一个大顶堆，然后将堆顶的最大值与最后一个元素交换，重新调整1~N-1元素，重新成为大顶堆，然后不断的重复这个步骤，最后堆长度会变成0，而剩下的就是有序数组了

堆可以看作是一棵完全二叉树，内部用数组维护元素，若i为root的下标，那么左子树为2&#42;i+1,右子树为2&#42;i+2;

大顶堆是每个节点的值都>=其左右孩子（如果有的话）值的完全二叉树

小顶堆便是每个节点的值都<=其左右孩子值的完全二叉树。

[之前的文章](../2015-10-28/java_concurrent02.html)介绍的PriorityBlockingQueue优先级队列内部就是用大顶堆来维护数据。

堆排序算法源码如下：

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import com.raven.sorts.Sort;

/**
 * 堆排序
 * @author Raven
 *
 * @param <T>
 */
public class HeapSort<T extends Comparable<T>> implements Sort<T> {

	@Override
	public void sort(T[] arr) {
		//构造一个最大堆
		//从第一个非叶子节点开始，第一个非叶子节点是（length-2)/2
		for(int start = (arr.length-2)/2; start>=0 ; start--){
			shiftDown(arr, start, arr.length-1);
		}
		//此时还不是有序的
		//还需要从根节点开始循环
		//每次从最大堆顶点取最大的值，与数组末尾的元素交换
		//然后重新构造最大堆
		for(int end = arr.length-1; end>0; end--){
			swap(arr, end, 0);
			//重新调整最大堆
			shiftDown(arr, 0, end-1);
		}
	}
	
	/**
	 * 自上向下构造最大堆
	 * @param arr
	 * @param start
	 * @param end
	 */
	private void shiftDown(T[] arr, int start, int end){
		int root, left, right, child;
		root = start; //子树根节点
		while(true){
			child = left = 2 * root + 1; //左子树
			if(left>end) break; //没有左子节点，由于是完全二叉树，此时直接结束循环
			if((right=left+1)<=end && arr[left].compareTo(arr[right])<0){
				//如果有右子节点，并且右子节点大于左子节点
				child = right;
			}
			//child为root中较大的子节点
			if(arr[root].compareTo(arr[child])<0){
				//root 小于 child
				swap(arr, root, child);
				root = child;
			} else {
				break;
			}
		}
	}
}</code>
</pre>

堆排序结果是:

Sort 10,Cost time:0ms

Sort 100,Cost time:0ms

Sort 1000,Cost time:1ms

Sort 10000,Cost time:4ms

Sort 100000,Cost time:40ms


###插入排序

有一个已经有序的数据序列，要求在这个已经排好的数据序列中插入一个数，但要求插入后此数据序列仍然有序，这个时候就要用到一种新的排序方法——插入排序法,插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，算法适用于少量数据的排序，时间复杂度为O(n^2)。是稳定的排序方法。插入算法把要排序的数组分成两部分：第一部分包含了这个数组的所有元素，但将最后一个元素除外，而第二部分就只包含这一个元素。在第一部分排序后，再把这个最后元素插入到此刻已是有序的第一部分里的位置

插入排序的源码：

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import com.raven.sorts.Sort;
/**
 * 插入排序
 * @author Raven
 *
 * @param <T>
 */
public class InsertSort<T extends Comparable<T>> implements Sort<T> {

	@Override
	public void sort(T[] arr) {
		for(int i=1;i<arr.length;i++){
			//此时0~(i-1)元素是有序的
			//我们需要把arr[i]插入到arr[0:i)这个有序序列中
			T tmp = arr[i];
			int j = i-1;
			while(j>=0 && arr[j].compareTo(tmp)>0){
				arr[j+1] = arr[j];
				j--;
			}
			arr[j+1] = tmp;
		}
	}
}
</code>
</pre>

运行结果：

Sort 10,Cost time:0ms

Sort 100,Cost time:1ms

Sort 1000,Cost time:6ms

Sort 10000,Cost time:132ms

Sort 100000,Cost time:14770ms

###希尔排序

> 希尔排序是1959 年由D.L.Shell 提出来的，相对直接排序有较大的改进。希尔排序又叫缩小增量排序

> 先将整个待排序的记录序列分割成为若干子序列分别进行直接插入排序，待整个序列中的记录“基本有序”时，再对全体记录进行依次直接插入排序。

先取一个小于n的整数d1作为第一个增量，把文件的全部记录分组。所有距离为d1的倍数的记录放在同一个组中。先在各组内进行直接插入排序；然后，取第二个增量d2<d1重复上述的分组和排序，直至所取的增量dt=1(dt<dt-l<…<d2<d1)，即所有记录放在同一组中进行直接插入排序为止。

shell排序时间复杂度依赖于步长序列，一般可以认为O(nlogn)

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import java.util.ArrayList;
import java.util.List;

import com.raven.sorts.Sort;

/**
 * 希尔排序
 * @author Raven
 *
 * @param <T>
 */
public class ShellSort<T extends Comparable<T>> implements Sort<T> {
	@Override
	public void sort(T[] arr) {
		List<Integer> steps = this.getSteps(arr.length);
		for(int step:steps){
			//步长step的插入排序
			//分step个新的序列
			// [0, step, 2*step ....]
			// [1, step+1, 2*step+1, ...]
			// [2, step+2, 2*step+2, ...]
			// ...
			// [step-1, 2*step-1 ...]
			//对每个序列进行插入排序
			for(int n = 0; n<step; n++){
				for(int i = n+step; i<arr.length; i+=step){
					T tmp = arr[i];
					int j = i - step;
					while(j>=0 && arr[j].compareTo(tmp)>0){
						arr[j+step]=arr[j];
						j-=step;
					}
					arr[j+step] = tmp;
				}
			}
		}
	}
	
	/**
	 * 根据数组长度计算增量序列n/2, n/4, n/8 ... 1
	 * @param length
	 * @return
	 */
	private List<Integer> getSteps(int length){
		List<Integer> ret = new ArrayList<>();
		length /= 2;
		while(length>0){
			ret.add(length);
			length /= 2;
		}
		return ret;
	}
}
</code>
</pre>

Shell排序运行结果是:

Sort 10,Cost time:0ms

Sort 100,Cost time:1ms

Sort 1000,Cost time:1ms

Sort 10000,Cost time:10ms

Sort 100000,Cost time:69ms

###归并排序

归并（Merge）排序法是将两个（或两个以上）有序表合并成一个新的有序表，即把待排序序列分为若干个有序的子序列，再把有序的子序列合并为整体有序序列。

<pre class="language-java line-numbers">
<code>
package com.raven.sorts.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.raven.sorts.Sort;
/**
 * 归并排序
 * @author Administrator
 *
 * @param <T>
 */
public class MergeSort<T extends Comparable<T>> implements Sort<T> {

	@Override
	public void sort(T[] arr) {
		//由于需要需要split分成两部分，所以把数组转为List，便于使用subList
		List<T> list = Arrays.asList(arr);
		Object[] tmp = split(list).toArray();
		//为了接口形式统一，这里将排序好的数据再拷贝回去
		//这个copy时间复杂度O(n)
		System.arraycopy(tmp, 0, arr, 0, arr.length);
	}
	
	/**
	 * 分裂
	 * @param arr
	 * @return
	 */
	private List<T> split(final List<T> arr){
		if(arr.size()<=1){
			return arr;
		}
		int mid = arr.size()/2;
		List<T> left = split(arr.subList(0, mid));
		List<T> right = split(arr.subList(mid, arr.size()));
		return merge(left, right);
	}
	
	/**
	 * 归并
	 * @param left
	 * @param right
	 * @return
	 */
	private List<T> merge(final List<T> left, final List<T> right){
		List<T> ret = new ArrayList<>(left.size()+right.size());
		int l = 0, r = 0;
		while(l&lt;left.size() && r &lt; right.size()){
			if(left.get(l).compareTo(right.get(r))<0){
				//左边的小，选左边
				ret.add(left.get(l));
				l++;
			} else {
				//右边小
				ret.add(right.get(r));
				r++;
			}
		}
		ret.addAll(left.subList(l, left.size()));
		ret.addAll(right.subList(r, right.size()));
		return ret;
	}
}
</code>
</pre>

运行结果:

Sort 10,Cost time:1ms

Sort 100,Cost time:1ms

Sort 1000,Cost time:9ms

Sort 10000,Cost time:28ms

Sort 100000,Cost time:212ms

---------------------

总结：

各种排序的稳定性，时间复杂度和空间复杂度总结：

![表格](../../images/2015-10-29/table.jpg)

我们比较时间复杂度函数的情况：

![曲线图](../../images/2015-10-29/graph.jpg)

---------------------

部分资料转自：

八大排序算法:[http://blog.csdn.net/hguisu/article/details/7776068](http://blog.csdn.net/hguisu/article/details/7776068)

