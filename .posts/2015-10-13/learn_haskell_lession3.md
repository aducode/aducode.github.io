<!--{layout:default title:haskell学习总结(三)::正则表达式}-->

haskell中的正则表达式用法<sup>[[1]](#reference1)</sup>

<pre class="language-haskell line-numbers">
<code>
-- 导入正则模块
Prelude>:module +Text.Regex.Posix 
-- 全部的正则操作基本都使用(=~)这一个函数操作  
Prelude Text.Regex.Posix>:t (=~) 	
(=~)
  :: (RegexContext Regex source1 target, 
      RegexMaker Regex CompOption ExecOption source) => 
	 source1 -> source -> target

-- 可见 (=~)的类型是非常复杂的， 
-- 但是我们使用起来确实非常方便，
-- 类似OO语言中的方法重载（根据返回值类型进行重载）

-- 显示指明返回值是Bool类型
Prelude Text.Regex.Posix>"hello world" =~ "hello" :: Bool
--返回True，说明"hello world" 匹配了正则"hello"
True

-- 显示的指明返回值是Int类型
Prelude Text.Regex.Posix>"hello world" =~ "l" :: Int
-- "l"在"hello world"中匹配到了3次
3
</code>
</pre>
通过上面简单的例子，可以看出对于不同类型的返回值，（=~）方法会进行不同的操作，返回对应类型的值，把复杂的操作都封装在模块内，
对外仅仅暴露一个简单的(=~)方法，这样的设计哲学值得学习！

关于(=~)更复杂的用法可以参考下面参考资料里的链接<sup>[[1]](#reference1)</sup>，这里就不再赘述了，其实写这篇文章的目的是想探讨一下(=~)内部到底做了什么，能够实现根据不同类型返回进行不同操作的。

个人感觉(没有读Text.Regex.Posix的源码，有时间是应该读一读的~)应该就是实现一个方法对RegexContext这个typeclass的不同实例进行封装，我自己模拟一个这样的方法来实现类似的功能：

<pre class="language-haskell line-numbers">
<code>
-- Context.hs
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE AllowAmbiguousTypes   #-}
module Context where

-- MultiParamTypeClasses扩展允许我们
-- 定义一个含有两个类型变量的typeclass
class Context source target where
	ret::source->target

-- FlexibleInstances扩展允许我们
-- 将String作为类型参数
instance Context String Bool where
	ret str = case str of 
		"yes" -> True
		otherwise -> False

instance Context String Int where
	ret str = case str of
		"one" -> 1
		otherwise -> 0

instance Context String String where
	ret s = s

instance Context Int Int where
	ret = (+) 1

instance Context Bool Bool where
	ret b = not b

instance Context Int Bool where
	ret i = case i of
		1 -> True
		otherwise -> False

instance Context Int String where
	ret i = (++) "Num:" (show i)

-- emit方法就会根据返回值和参数的类型调用不同的Cotext的实例的ret方法
emit::(Context source target) => source->target
emit = ret
</code>
</pre>

使用我们emit方法:
<pre class="language-haskell line-numbers">
<code>
Prelude>:load Context.hs
*Contex>emit True::Bool
False
*Context>emit (1::Int)::Bool
True
*Context>emit "hello"::String
"hello"
*Context>emit "yes"::Bool
True
</code>
</pre>

这只是我猜测的实现，真正的实现不一定是这样，或者比这个复杂的多的多。。。

关于FlexibleInstances扩展请见[stack overflow第二个回答](http://stackoverflow.com/questions/15285822/cant-make-string-an-instance-of-a-class-in-haskell/15286372)


------

**参考资料**

<a name="reference1" id="reference1">

1. [real world in haskell](http://book.realworldhaskell.org/read/efficient-file-processing-regular-expressions-and-file-name-matching.html#glob.regex)

------

**haskell学习总结**

* [开始学习Haskell](../2015-06-12/begin_haskell.html)
* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
* [haskell学习总结(三)::正则表达式](../2015-10-13/learn_haskell_lession3.html)
* [haskell学习总结(四)::强大的Parsec](../2015-10-21/learn_haskell_lession4.html)
