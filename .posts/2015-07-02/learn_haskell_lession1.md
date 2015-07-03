<!--{layout:default title:haskell学习总结(一)}-->
前段时间看完了[haskell趣学指南](http://learnyoua.haskell.sg/),了解了一些haskell的基本语法和函数式编程的皮毛。不过说实话，haskell的学习曲线确实比较陡，加上我大学学的数学理论基本都还给老师了，所以一些概念理解起来着实困难。

俗话说好记性不如烂笔头，现在就将已经学到的haskell知识整理总结一下

##搭建开发环境
可以从[haskell官网](https://www.haskell.org/)中找到haskell platform的下载地址。
haskell的开发环境主要包括:

* GHCi：交互式命令行
* GHC： Haskell的编译器（将.hs源码编译成不同* * 平台下的可执行程序）
* cabal： 包管理工具&构建工具，就像Java理的[Maven](http://maven.apache.org/), Python里的[pip](https://pypi.python.org/pypi)
* runhaskell: 解释引擎，可以将haskell作为脚本解释执行
* 常用模块

##Hello World
<pre class="language-haskell line-numbers">
<code>
{-
    helloworld.hs
-}
main::IO ()
main = do
    -- display hello world
    putStrLn "hello world"
</code>
</pre>
学习语言的第一件事当然就是写出HelloWorld了,将上面一段代码保存在helloworld.hs文件中，然后执行
<pre class="language-bash line-numbers">
<code>
ghc -o helloworld helloworld.hs
./helloworld
</code>
</pre>
就会在屏幕中显示出"hello world"
##基本语法
###注释

单行注释: --

多行注释 {- -}

多行注释还可以声明一些GHCi扩展，比如：

{-#LANGUAGE OverloadedStrings#-}

{-#LANGUAGE QuasiQuotes#-}

{-#LANGUAGE TemplateHaskell#-}

{-#LANGUAGE TypeFamilies#-}

###类型
####基本类型
Haskell是静态类型语言，但是有非常强大的类型推导，所以不需要向java或者C语言那样，必须写明声明变量的类型。
Haskell 编译器可以自动推断出程序中几乎所有表达式的类型[注：有时候要提供一些信息，帮助编译器理解程序代码]。这个过程被称为类型推导（type inference）。
虽然 Haskell 允许我们显式地为任何值指定类型，但类型推导使得这种工作通常是可选的，而不是非做不可的事。。
haskell中的基本类型主要有：

* Char

单个 Unicode 字符。

* Bool 

表示一个布尔逻辑值。这个类型只有两个值： True 和 False 。

* Int

带符号的定长（fixed-width）整数。这个值的准确范围由机器决定：在 32 位机器里， Int 为 32 位宽，在 64 位机器里， Int 为 64 位宽。Haskell 保证 Int 的宽度不少于 28 位。

* Integer

不限长度的带符号整数。 Integer 并不像 Int 那么常用，因为它们需要更多的内存和更大的计算量。另一方面，对 Integer 的计算不会造成溢出，因此使用 Integer 的计算结果更可靠。

* Double

用于表示浮点数。长度由机器决定，通常是 64 位。（Haskell 也有 Float 类型，但是并不推荐使用，因为编译器都是针对 Double 来进行优化的，而 Float 类型值的计算要慢得多。）

####列表
列表容器要求内部的元素类型完全一致[Int] 表示Int列表类型 [Char]表示字符列表**也就是String类型**，其他类型的列表以此类推

####自定义新的数据类型
使用data关键字可以定义新的数据类型
<pre class="language-haskell line-numbers">
<code>
data Person = Person
</code>
</pre>
以上代码定义了一个Person类型的数据，然后这个类型中没有保存任何数据
<pre class="language-haskell line-numbers">
<code>
data Person = Person String Int
</code>
</pre>
这样定义Person类型，可以保存两种数据:String类型和Int类型
**注意**:上面代码等号左边的Person是类型，右边Person叫做构造函数(constructor)，左右并不一定要名字一致，而且构造函数可以有多个，之间用"|"隔开
<pre class="language-haskell line-numbers">
<code>
data Person = Student String Int | Teacher String Int Double
</code>
</pre>
Person是类型,Student是一个构造函数(Student::String->Int->Person),Teacher也是一个构造函数(Teacher::String->Int->Double->Person)
<pre class="language-haskell line-numbers">
<code>
let person1 = Student "XiaoMing" 12
let person2 = Teacher "LaoZhang" 30  5000
</code>
</pre>
这样person1和person2就都是Person类型数据了
若要取Person类型中的名字，我们可以定义这样的函数
<pre class="language-haskell line-numbers">
<code>
getName::Person->String
getName (Student name _) = name
getName (Teacher name _  _) = name

getName (Teacher "LaoZhang" 30 5000)
</code>
</pre>
为了自定义类型用起来方便，haskell还提供了另外一种构造函数(haskell的语法糖)
<pre class="language-haskell line-numbers">
<code>
-- 注意字段之间的逗号
data Person = Student{name::String,age::Int}|Teacher{name::String,age::Int,wage::Double}
let person1 = Student{name="XiaoMing", age=12}
let person2 = Teacher{name="LaoZhang", age=30, wage=5000}
name person2
</code>
</pre>
用这种构造函数，haskell会自动生成相应的取值函数，比如name::Person->String  age::Person->Int

###函数
####函数声明
比如上面helloworld程序中:
<pre class="language-haskell line-numbers">
<code>
main::IO ()
</code>
</pre>
表示main函数是没有参数，并且返回IO ()类型的函数
再来看看下面的函数
<pre class="language-haskell line-numbers">
<code>
add::Int->Int->Int
</code>
</pre>
这条语句声明了一个add函数，它接收两个Int类型的参数，返回一个Int类型的结果

当然以上是一种理解方式，对于函数式编程思想，应该是这样理解的：

add函数，接收一个Int类型的参数，返回一个偏函数（返回的函数类型是接收Int类型，产生Int结果）
可以这样认为：**Haskell中的函数都是只有一个参数，并且只产生一个结果**。

另外注意一点：**haskell的函数声明不是必须的，函数类型可以推导出来**，也就是说main::IO ()这句可以省略：）
####函数的实现
如上面helloworld程序
<pre class="language-haskell line-numbers">
<code>
main = do
    putStrLn "hello world"
</code>
</pre>
这就是函数的实现 函数名 [参数列表]= 函数体
再来看看add的实现：
<pre class="language-haskell line-numbers">
<code>
add x y = x + y
</code>
</pre>
可以看到add接受两个参数 x y 然后将x+y的结果作为结果
当然，一个函数可以有多个实现，比如这样：
<pre class="language-haskell line-numbers">
<code>
add 0 0 = 100
add x y = x + y
</code>
</pre>
对于上面add函数
add 0 0的结果是 100
add 0 1的结果是 1

----------------------
###未完待续
