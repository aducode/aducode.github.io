<!--{layout:default title:常见排序算法}-->

最近正在准备找工作，感觉面试过程中好多人喜欢问排序算法（吐槽一下，虽然大部分公司内的代码根本就不会用到这些算法），于是就在这里整理一下，同时也为面试做做准备吧。

之前整理并且用python实现了这些排序算法[[点此下载python版]](../../attachments/2015-10-29/python-sort.zip),今天就用Java实现一遍吧！

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

---------------------

未完待续

