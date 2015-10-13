<!--{layout:default title:haskell学习总结(一)::初级篇}-->
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

多行注释还可以声明一些GHCi[扩展](https://wiki.haskell.org/Language_extensions)，比如：

{-#LANGUAGE OverloadedStrings#-}

{-#LANGUAGE QuasiQuotes#-}

{-#LANGUAGE TemplateHaskell#-}

{-#LANGUAGE TypeFamilies#-}

以下是另一种写法

{-# OPTIONS_GHC -XTypeFamilies -XTemplateHaskell -XQuasiQuotes #-}

在GHCI控制台情况下要使用扩展，可以使用:set命令:
<pre class="language-bash line-numbers">
<code>
Prelude>:set -XOverloadedStrings
Prelude>:set -XQuasiQuotes
Prelude>:set -XTemplateHaskell
Prelude>:set -XTypeFamilies
</code>
</pre>

或者在启动GHCi的时候加上-X

<pre class="language-bash line-numbers">
<code>
ghci -XOverloadedStrings -X TemplateHaskell -ddump-splices
# If you want to see the expansion of splices, 
# use the flag -ddump-splices when starting GHCi
</code>
</pre>

关于扩展的资料详见[24 Days of GHC Extensions](https://ocharles.org.uk/blog/pages/2014-12-01-24-days-of-ghc-extensions.html)


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

####类型别名
haskell中可以用上C语言的typeof类似的功能，给现有的类型起个别名，比如：
<pre class="language-haskell line-numbers">
<code>
type Age = Int
type String = [Char]
type IntList = [Int]
</code>
</pre>
上面第二行，其实haskell内部已经帮我们做了

####自定义新的数据类型
使用data关键字可以定义新的数据类型
<pre class="language-haskell line-numbers">
<code>
-- 定义了一种新的类型Test
-- 但是他没有构造函数，只能用作类型参数
data Test

--定义了一种新的类型Person，构造函数也是Person
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
data Person = Student{name::String,age::Int}
			|Teacher{name::String,age::Int,wage::Double}
let person1 = Student{name="XiaoMing", age=12}
let person2 = Teacher{name="LaoZhang", age=30, wage=5000}
name person2
</code>
</pre>
用这种构造函数，haskell会自动生成相应的取值函数，比如name::Person->String  age::Person->Int

类型也可以带参数(不是构造函数带参数哦~)，就像这样：
<pre class="language-haskell line-numbers">
<code>
data Entry a b = Entry{key::a,value::b}
let p1 = Entry 1 "Foo"
let p2 = Entry "Bar" 3.5
let p3 = Entry{key="A",value="HHHH"}
let p4 = Entry (1::Double)  2
let p5 = Entry{key=1::Double, value=2}
</code>
</pre>
上面的Entry中可以保存任何类型的a和b

除了上面标准的data用法外，还可以使用[Generalised algebraic datatype(GADT)](https://wiki.haskell.org/GADT)
<pre class="language-haskell line-numbers">
<code>
{-# LANGUAGE GADTs #-}
data Person where
	Student::String->Int->Person
	Teacher::String->Int->Double->Person
	

data Entry a b where
	--前面的Entry是构造函数名 后面的Entry是定义的new type名称
	Entry::a->b->Entry 

--使用GADTs还可以添加更多的类型限定
data E a where
	A::Eq b=>b->E b
</code>
</pre>

Record Wildcards扩展，可以让代码更简洁
<pre class="language-haskell line-numbers">
<code>
{-# LANGUAGE RecordWildCards	#-}
data Person = Person{
        name::String,
        age::Int
}deriving(Show)

getPerson::IO Person
getPerson = return $ Person "Duyang" 13

main::IO ()
main = do
		-- 不使用扩展
		person <- getPerson
		putStrLn $ show $ name person
		putStrLn $ show $ age person
		-- 使用扩展,其中person2代表匹配到的Person类型整体
        person2@Person {..} <- getPerson
        putStrLn $ show name
		putStrLn $ show age
		putStrLn $ show person2					
</code>
</pre>

###类型类
haskell中用data关键字可以像c语言中定义struct一样，同时也提供一种类似java**接口**的类型类，使用class关键字
####一般情况
<pre class="language-haskell line-numbers">
<code>
--跟在class之后的Animal是这个类型类的名字，之后的a是这个类型类的实例类型(instance type)
-- 注意 默认情况下(无扩展)haskell的类型类必须有一个类型变量
-- 也就是在Prelude中:k Animal结果必须是 Animal :: *->Constraint
class Animal a where
	eat::a->String->String
data Pet = Cat | Dog

--相当于java中Pet类实现Animal接口
instance Animail Pet where
	eat Cat food = "Cat eat " ++ food
	eat Dog food = "Dog eat " ++ food

let pet1 = Cat
eat pet1 "fish"
let pet2 = Dog
eat pet2 "meat"
</code>
</pre>

####扩展:[Nullary Type Classes](https://ocharles.org.uk/blog/posts/2014-12-10-nullary-type-classes.html)

<pre class="language-haskell line-numbers">
<code>
{-# LANGUAGE NullaryTypeClasses  #-}
-- 使用上面这个扩展之后，没有类型变量的类型类变得合法了

-- 这里的类型类是没有类型参数的
-- :k Animal的结果是：Animal :: Constraint
class Animal where
	eat::String->String
	
-- 在需要的时候实现Animal
instance Animal where
	eat food = "eat " ++ food

main::IO ()
main = do
	putStrLn $ eat "Apple"
	-- It will display:  eat Apple
</code>
</pre>

####扩展:[Multi-parameter Type Classes](https://ocharles.org.uk/blog/posts/2014-12-13-multi-param-type-classes.html)

<pre class="language-haskell line-numbers">
<code>
{-# LANGUAGE MultiParamTypeClasses #-}
-- 使用上面这个扩展之后，有多个类型变量的类型类变得合法了

-- 类型类可以有多个类型变量（这里是3个）
-- :k Animal的结果是 Animal :: * -> * -> * -> Constraint
class Animal a b c where
        act::a->b->c->String

data Pet = Dog | Cat

data Food = Meat | Fish

data Action = Eat | Sleep

instance Animal Pet Action Food where
        act Dog Eat Meat = "Dog eat meat..."
        act Cat Eat Fish = "Cat eat fish..."
        act _ _ _ = "Invalidate!"

main::IO ()
main = do
        putStrLn $ act Dog Eat Meat
		-- Dog eat meat...
        putStrLn $ act Cat Eat Fish
		-- Cat eat fish...
        putStrLn $ act Dog Eat Fish
		-- Invalidate!
        putStrLn $ act Cat Eat Meat
		-- Invalidate!
        putStrLn $ act Cat Sleep Fish
		-- Invalidate!
</code>
</pre>

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

这就叫函数的**模式匹配(Pattern matching)**

模式匹配一般也可以用**Case expressions**来实现：
<pre class="language-haskell line-numbers">
<code>
add x y = case  x y of 
			0 0 -> 100
			otherwise -> x+y	
</code>
</pre>
再看如下代码
<pre class="language-haskell line-numbers">
<code>
bmiTell :: (RealFloat a) => a -> String  
bmiTell bmi  
    | bmi <= 18.5 = "You're underweight, you emo, you!"  
    | bmi <= 25.0 = "You're supposedly normal. Pffft, I bet you're ugly!"  
    | bmi <= 30.0 = "You're fat! Lose some weight, fatty!"  
    | otherwise   = "You're a whale, congratulations!"  
</code>
</pre>
这叫做**Guard**
>guard 由跟在函数名及参数后面的竖线标志，通常他们都是靠右一个缩进排成一列。一个 guard 就是一个布尔表达式，如果为真，就使用其对应的函数体。如果为假，就送去见下一个 guard，如之继续。如果我们用 24.3 呼叫这个函数，它就会先检查它是否小于等于 18.5，显然不是，于是见下一个 guard。24.3 小于 25.0，因此通过了第二个 guard 的检查，就返回第二个字串。

####分支控制
上面的case of 与Guard可以看做其他语言的case，那么haskell有没有if呢？
haskell中也有if，但是与java 或者c等其他面向对象、面向流程的语言来说，haskell的if else是表达式（expression不是statement），主要表现在else是不可以省略的。

if的完整形式是: if ... then ... else ...
<pre class="language-haskell line-numbers">
<code>
add x y = if x==0 && y==0
			then 100
			else  x + y
</code>
</pre>

####Lambda

haskell中也支持lambda语法(可以认为是匿名函数啦)

<pre class="language-haskell line-numbers">
<code>
-- 下面的语法定义了一个lambda表达式，
-- 最终结果将是101
(\x->x+1) 100

-- 下面定义了一个接受两个参数的lambda表达式，
-- 两个参数之间以空格分隔， 
-- 最终结果是3
(\x y->x+y) 1 2

-- 接受两个参数的lambda的另外一种写法，
-- 注意\x-> \y-> 之间的空格， 
-- 最终结果是3
(\x-> \y->x+y) 1 2


-- lambda 的应用
-- :t map
-- map::(a->b)->[a]->[b]
map (\x->x+100) [1..10]
--结果是 [101,102,...110]
</code>
</pre>

注意上面接受两个参数的第二种写法一定要注意空格，否则：
![img](../../images/2015-07-02/syntax_error.jpg)

####列表推导式(List comprehension)

python语言可以这样写：
<pre class="language-python line-numbers">
<code>
[(x,y) for x in xrange(10) for y in xrange(10)]
</code>
</pre>

haskell语言中语法如下:
<pre class="language-haskell line-numbers">
<code>
[(x,y)|x<-[0..9], y<-[0..9]]
</code>
</pre>

####自定义操作符

定义一个运算符, 要说明它的结合性和优先级.
   
>   infixr 右结合

>   infixl 左结合

>   infix  不结合
   
左右都可结合的运算符如 +, * 定义为左结合即可.

优先级从0到9, 0最低, 9最高   

已定义的运算符有:
   
>   level 9 . and !!

>   level 8 ^

>   level 7 *, /, &#96;div&#96;, &#96;rem&#96; and &#96;mod&#96;

>   level 6 + and -

>   level 5 :, ++ and \

>   level 4 ==, /=,<, <=, >, >=, &#96;elem&#96; and &#96;notElem&#96;

>   level 3 &&

>   level 2 ||

>   level 1 (not used in the prelude)
   
举例:
<pre class="language-haskell line-numbers">
<code>    
   infixr 3  &&                       
   (&&)  :: Bool -> Bool -> Bool
   False && x   = False
   True  && x   = x         

   -- 先定义&&的结合性和优先级, 然后象定义函数一样定义它的功能.
   
   -- 运算符用括号括起来, 可以当作函数使用, 比如:
   
   map (3+) [1,2,3]
   
   map (+3) [1,2,3]
   
   -- 函数名用左引号`引起来, 也可以声明为运算符, 比如:
   
   fac n = product [1..n]

   infix 5 !^!, `choose`
   (!^!), choose :: Int->Int->Int                   
   n `choose` k = fac n `div` (fac k * fac (n-k))
   n !^! k = fac n `div` (fac k * fac (n-k))     
   
   -- 有了这些定义后,
   
   choose 5 2
   (!^!)  5 2
   5   !^!  2
   5 `choose` 2
   
   -- 都给出答案10.  
</code>
</pre>

###模块(Module)

Module是haskell源码的组织方式，可以将功能解耦到不同的Module中。

Module可以是被组织成树形，与树形文件系统基本一致，让我们来看个具体例子：

目录结构如下：

<pre class="language-bash line-numbers">
<code>
`
|-----Dict0                           #第一级目录
|       |-----Dict1                  #第二级目录
|       |       `-----Test0.hs        #Haskell源码文件Test0.hs
|       `-----Test1.hs                #Haskell源码文件Test1.hs
|------Test2.hs                       #Haskell源码文件Test2.hs
`------Main.hs                        #Haskell入口所在源码文件Main.hs
</code>
</pre> 

Test0.hs内容如下：

<pre class="language-haskell line-numbers">
<code>
-- Test0.hs
module Dict0.Dict1.Test0 where
say::String
say = "hello world"

foo::Int
foo = 42

</code>
</pre>

Test1.hs内容如下:

<pre class="language-haskell line-numbers">
<code>
-- Test1.hs
module Dict0.Test1 where

bar::String
bar = "Bar!!!!"

say::String 
say = "hello world!In Test1"
 
</code>
</pre>

Test2.hs内容如下:

<pre class="language-haskell line-numbers">
<code>
-- Test2.hs
module Test2(Tree(Leaf, TreeNode), Node(..), test) where
-- Tree(Leaf, TreeNode) 表示Tree类型的Leaf TreeNode两个构造函数被export
-- Node(..) 表示Node类型全部构造函数都被export
data Node = MyInt Int|MyText String deriving(Show)

data Tree = Leaf|TreeNode Node Tree Tree |PrivateLeaf deriving(Show)

test::String
test = "Hi this is TEST"

-- test2相当于Test2模块的私有函数，不能被其他模块import
test2::String
test2 = "Hi this is TEST2"
</code>
</pre>

Main.hs内容如下:

<pre class="language-haskell line-numbers">
<code>
-- Main.hs
-- import Dict0.Dict1.Test0 -- Dict0.Dict1.Test0中的say 和 foo都可用
import Dict0.Dict1.Test0 (say)  -- Dict0.Dict1.Test0 中的foo将不可用
-- import qualified Dict0.Test1  -- 不能直接使用Test1中的函数，需要写全
import qualified Dict0.Test1 as T -- T作为Dict0.Test1的别名
import Test2

main::IO ()
main = do
    putStrLn say
    -- putStrLn foo  --错误，作用域内没有foo函数
    putStrLn T.say
    putStrLn test
    putStrLn $ show Leaf
    putStrLn $ show $ TreeNode (MyInt 42) Leaf Leaf
    -- putStrLn $ PrivateLeaf --错误，作用域内没有PrivateLeaf构造函数
    -- putStrLn test2 -- 错误，作用域内没有test2
</code>
</pre>

###Prelude tips

Prelude是haskell语言的命令行交互界面，这里记录一些常用的操作吧：

* 退出Prelude(第一次都不知道怎么退出T T) :q
* Prelude启用扩展 :set -Xxxxx
* it用法

> it is a special variable in ghci that allows us to reference the last computed value.


------------

**haskell学习总结**

* [开始学习Haskell](../2015-06-12/begin_haskell.html)
* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
* [haskell学习总结(三)::正则表达式](../2015-10-13/learn_haskell_lession3.html)