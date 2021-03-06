<!--{layout:default title:Java8 Stream操作}-->
参考：

* [http://ifeve.com/stream/](http://ifeve.com/stream/)
* [http://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html](http://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html)

学习java8中Stream的操作，自己做了一些测试代码如下：
<pre  class="language-java line-numbers"><code>
package test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class NewFeature {
    //java8的新特性
	public static void main(String [] args){
		class Gen{
			private int i;
			public Gen(int value){
				i=value;
			}
			public Integer get(){
				return i--;
			}
			
			
		}
		Integer [] iArray={0,1,1,1,2,3,4,5,6,7,8,9};
		List<Integer> list = Arrays.asList(iArray);
		/**
		 * Stream 的转换
		 * */
		//distinct
		System.out.println("========== test distinct ====================");
		list.stream().distinct().forEach(System.out::println);
		//filter
		System.out.println("========== test filter ====================");
		list.stream().filter(x->x<5).forEach(System.out::println);
		//map
		System.out.println("========== test map ====================");
		list.stream().map(x->x*10).forEach(System.out::println);
		//flatMap
		System.out.println("========== test flatMap ====================");
		//<R> Stream<R> flatMap(Function<? super T,? extends Stream<? extends R>> mapper)
		//flatMap与map的区别是 map将每个元素做一些简单的转化（如上面*10）  flatMap则会对每一个元素生成一个新的stream，合并到旧的stream中
		list.stream().flatMap(x->{
			Gen gen = new Gen(x);
			return Stream.generate(gen::get).limit(x+1);//如 Gen(9) 则会产生一个 [9,8,7,6,5,4,3,2,1,0] 的stream
		}).forEach(System.out::println);
		//peek
		System.out.println("========== test peek ====================");
		list.stream().peek(x->{System.out.println("hi~ I'm in peek["+x+"}");}).forEach(x->{});
		list.stream().peek(x->{System.out.println("hi~ I'm in peek["+x+"}");}).forEach(System.out::println);
		//limit
		System.out.println("========== test limit ====================");
		list.stream().limit(5).forEach(System.out::println);
		//skip
		System.out.println("========== test skip ====================");
		list.stream().skip(5).forEach(System.out::println);
		//sorted
		System.out.println("========== test sorted ====================");
		list.stream().sorted().forEach(System.out::println);
		System.out.println("========== test sorted2 ====================");
		list.stream().sorted((a,b)->b.compareTo(a)).forEach(System.out::println);
		/**
		 * 汇聚
		 * */
		//collect
		System.out.println("========== test collect ====================");
		//<R> R collect(Supplier<R> supplier,
	    //          BiConsumer<R,? super T> accumulator,
	    //          BiConsumer<R,R> combiner)
		//supplier = ()->new ArrayList<Integer>()  工厂类，生成容器
		//accumulator = (l,item)->l.add(item)  l是之前工厂类生成的，item是每个元素  将元素添加到新生成的容器
		//combiner 并行stream中使用 parallelStream()中生效，最终做合并操作
		System.out.println(list.stream().collect(()->new ArrayList<Integer>(),(l,item)->l.add(item*5),(l1,l2)->l1.addAll(l2)));
		//list.stream().collect(ArrayList::new,(l,item)->l.add(item*10),(l1,l2)->l1.addAll(l2));
		System.out.println("========== test collect 2 ====================");
		System.out.println(list.stream().collect(Collectors.toList()));
		//reduce
		System.out.println("========== test reduce ====================");
		Integer res1 = list.stream().reduce((x,y)->x+y).get();
		System.out.println("reduce res1 is:"+res1); //0+1+1+1+2+3+4+5+6+7+8+9
		Integer res2 = list.stream().reduce(100, (x,y)->x+y);
		System.out.println("reduce res2 is:"+res2); //100 + 0+1+1+1+2+3+4+5+6+7+8+9
		String res3 = list.stream().reduce("result is:",(a,b)->a+"--"+b,(x,y)->x+","+y);
		System.out.println("reduce res3 is:"+res3); //result is:--0--1--1--1--2--3--4--5--6--7--8--9
		//combiner 参数是在并行stream中生效，如下parallelStream
		//每个并行的stream初始值是"result is" 并且确定为String类型
		//每个并行的Stream会使用accumulator = (a,b)=>a+"--"+b  将两两元素变成Stream类型
		//combiner = (x,y)->x+","+y  在所有并行stream操作完后最终合并
		String res4 = list.parallelStream().reduce("result is:",(a,b)->a+"--"+b,(x,y)->x+","+y);
		System.out.println("reduce res4 is:"+res4); //reduce res4 is:result is:--0--1--1,result is:--1--2--3,result is:--4--5--6,result is:--7--8--9
		//all Match
		System.out.println("========== test allMatch ====================");
		boolean isAllMatch = list.stream().allMatch((x)->x>0);
		//boolean isAllMatch = list.parallelStream().allMatch((x)->x>=0);
		System.out.println("isAllMatch:"+isAllMatch); //false  0>0
		//anyMatch
		System.out.println("========== test anyMatch ====================");
		boolean isAnyMatch = list.stream().anyMatch((x)->x>0);
		System.out.println("isAnyMatch:"+isAnyMatch); //true
		//noneMatch
		System.out.println("========== test noneMatch ====================");
		boolean isNoneMatch  = list.stream().noneMatch((x)->x>0);
		System.out.println("isNoneMatch:"+isNoneMatch); //false  是否所有元素都不满足要求
		//findFirst
		System.out.println("========== test findFirst ====================");
		Integer first = list.stream().findFirst().get();
		System.out.println("first is:"+first);
		//findAny
		System.out.println("========== test findAny ====================");
		Integer any=list.stream().findAny().get();
		System.out.println("any is:"+any);
//		Integer any2 = Arrays.asList(new Integer[]{}).stream().findAny().get();
//		System.out.println("any2 is:"+any2);
		//max min
		System.out.println("========== test max min====================");
		Integer max = list.stream().max((a,b)->a.compareTo(b)).get();
		System.out.println("max is:"+max);
		Integer min = list.stream().min((a,b)->a.compareTo(b)).get();
		System.out.println("min is:"+min);
		//count
		System.out.println("========== test count====================");
		long count = list.stream().count();
		System.out.println("count is:"+count);
		//forEach
		System.out.println("========== test forEach====================");
		list.stream().forEach(System.out::print);
		System.out.println();
		Arrays.asList(new Integer[]{3,2,1,4}).stream().forEachOrdered(System.out::print);
	}
}
</code></pre>
###从文件中获取Stream
需要自己实现Spliterator接口，然后使用StreamSupport.stream(Spliterator spliterator, boolean pallel)方法

<pre class="language-java line-numbers"><code>
package test;

import java.util.Spliterator;
import java.util.function.Consumer;
import java.util.stream.StreamSupport;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;


public class StreamTest {
    public static class FileSpliterator implements Spliterator<String>{
		private BufferedReader reader = null;
		public FileSpliterator(String filename){
				try {
	                this.reader = new BufferedReader(new FileReader(filename));
                } catch (FileNotFoundException e) {
	                e.printStackTrace();
                }
		}
		@Override
        public boolean tryAdvance(Consumer<? super String> action) {
			if(this.reader==null){
				return false;
			}
	        String line;
            try {
	            line = reader.readLine();
	            if(line!=null){
		        	action.accept(line);
		        	return true;
		        } else {
		        	if(this.reader!=null){
		        		this.reader.close();
		        	}
		        	return false;
		        }
            } catch (IOException e) {
	            e.printStackTrace();
	            if(this.reader!=null){
	            	try {
	                    this.reader.close();
                    } catch (IOException e1) {
	                    e1.printStackTrace();
                    }
	            }
	            return false;
            }
        }

		@Override
        public Spliterator<String> trySplit() {
			return null;
        }

		@Override
        public long estimateSize() {
			return 0;
        }

		@Override
        public int characteristics() {
			//表明是一个不可变的Spliterator
	        return IMMUTABLE;
        }
		
	}
	public static void main(String [] args) throws Exception{
		StreamSupport.stream(new FileSpliterator("D:\\test.txt"), false).filter(x->!x.isEmpty()).forEach(System.out::println);
	}
}
</code></pre>
