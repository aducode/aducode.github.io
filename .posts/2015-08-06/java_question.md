<!--{layout:default title:Java tricky question }-->
原文：[4 out of 5 Java developers failed to solve this question](https://jaxenter.com/4-out-of-5-java-developers-failed-to-solve-this-question-119321.html?ref=dzone)
###1. The toughest question of the Java deathmatch
![img](../../images/2015-08-06/question1.png)

正确答案：Compliation fails because no SQLException is thrown

关于java泛型[类型擦除](http://blog.csdn.net/caihaijiang/article/details/6403349)的问题。

###2. toString(), or not toString(), that is the question
![img](../../images/2015-08-06/question2.png)
类没有实现toString的小陷阱

正确答案：None of the above

###3. Google Guava Sets
![img](../../images/2015-08-06/question3.png)

正确答案：Potential out of memory

###4. Double brace initialization, lol wut?!
![img](../../images/2015-08-06/question4.png)

正确答案：Potential null access

参考[Double Brace Initialization](http://www.c2.com/cgi/wiki?DoubleBraceInitialization)，集合{{}}的形式相当于匿名内部类，NAMES.add的时候还没实例化完成。。

正确的写法：
<pre class="language-java line-numbers">
<code>
private static final List<String> NAMES = new ArrayList<String>(){{
	add("Hello");
	this.add("World");
	System.out.println(this); //这里用NAMES的话是null
}};
</code>
</pre>

###5. The curious case of the map at runtime
![img](../../images/2015-08-06/question5.png)

正确答案：[] true

###Bonus: And the easiest question is…
![img](../../images/2015-08-06/question6.png)

正确答案：C