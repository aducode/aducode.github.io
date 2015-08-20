<!--{layout:default title:haskell学习总结(二)::元编程}-->
上一篇总结了一下haskell中的基本语法，这篇打算总结一下haskell中的**元编程:**TemplateHaskell<sup>[[1]](#reference1)</sup><sup>[[2]](#reference2)</sup><sup>[[3]](#reference3)</sup>

> The essence of Template Haskell is to write Haskell code that generates new Haskell code. To ensure that the generated code is well structured, we don't generate Haskell source code, but instead generate the abstract syntax trees directly. 

> Template Haskell的本质是用haskell生成haskell代码。为了保证生成有结构的代码，不生成haskell源码，而是生成抽象语法树(AST)

###引子
首先看一个使用TemplateHaskell扩展的经典例子，实现一个haskell中的[printf函数](https://ocharles.org.uk/blog/guest-posts/2014-12-22-template-haskell.html)：

<pre class="language-haskell line-numbers">
<code>
-- Main.hs
{-# LANGUAGE TemplateHaskell #-}
module Main where
import PrintF (printf)

main::IO ()
main = do
	-- :t printf
	-- printf :: String -> Q Exp
	putStrLn $ $(printf "hello,%s\nthe Answer to Life, the Universe and Everthing is %d") "Issac" 42
	-- putStrLn ($(printf "hello,%s\nthe Answer to Life, the Universe and Everthing is %d") "Issac" 42)
</code>
</pre>

<pre class="language-haskell line-numbers">
<code>
-- PrintF.hs
{-# LANGUAGE TemplateHaskell #-} -- 这里要启用TemplateHaskell扩展
module PrintF where

-- NB: printf needs to be in a separate module to the one where
-- you intend to use it.

-- Import some Template Haskell syntax
import Language.Haskell.TH

-- Possible string tokens: %d %s and literal strings
data Format = D | S | L String
    deriving Show

-- a poor man's tokenizer
tokenize :: String -> [Format]
tokenize [] = []
tokenize ('%':c:rest) | c == 'd' = D : tokenize rest
                      | c == 's' = S : tokenize rest
tokenize (s:str) = L (s:p) : tokenize rest -- so we don't get stuck on weird '%'
    where (p,rest) = span (/= '%') str

-- generate argument list for the function
args :: [Format] -> [PatQ]
args fmt = concatMap (\(f,n) -> case f of
                                  L _ -> []
                                  _   -> [varP n]) $ zip fmt names
    where names = [ mkName $ 'x' : show i | i <- [0..] ]

-- generate body of the function
body :: [Format] -> ExpQ
body fmt = foldr (\ e e' -> infixApp e [| (++) |] e') (last exps) (init exps)
    where exps = [ case f of
                    L s -> stringE s
                    D   -> appE [| show |] (varE n)
                    S   -> varE n
                 | (f,n) <- zip fmt names ]
          names = [ mkName $ 'x' : show i | i <- [0..] ]

-- glue the argument list and body together into a lambda
-- this is what gets spliced into the haskell code at the call
-- site of "printf"
printf :: String -> Q Exp
-- lamE::[PatQ] -> ExpQ -> ExpQ 
-- 会生成一个lambda表达式 
-- let myLambdaExp = lamE [varP $ mkName "x", varP $ mkName "y"] (infixApp (varE $ mkName "x") [|(+)|] (varE $ mkName "y"))
-- let myLambda = $(myLambdaExp)
-- 相当于生成
-- \x y->x+y 的lambda表达式
-- myLambda 1 2  -----> 结果为3
-- myLambdaExp的另一种写法
-- let myLambdaExp' = [|\x y->x+y|]
printf format = lamE (args fmt) (body fmt)
    where fmt = tokenize format
</code>
</pre>

###Haskell  AST

####Quotation

TemplateHaskell扩展和Language.haskell.TH模块，主要用来生成AST（抽象语法树），然后再使用$() 对抽象语法树进行求值（或者说编译AST，生成Haskell可执行表达式或类型）

AST中的主要构成元素有：Expression  Declaration Type Pattern
这些元素可以方便的用Quotation表示出来：

#####Expression
> [|...|] or [e|...|] "..." is an expression; the quotation has type Q Exp.

> Expression quotations are used for generating regular Haskell expressions, and the have the syntax [|expression|]. So for example [|1+2|] is syntactic sugar for the infix expression InfixE (Just (LitE (IntegerL 1))) (VarE GHC.Num.+) (Just (LitE (IntegerL 2))).
可以在TemplateHaskell中用 Oxford brackets(牛津括号，什么鬼)括起来表示: [e|1+1|] or [|1+1|]

#####Declaration
> [d|...|]  "..." is a list of top-level declarations, the quotation has type Q [Dec]. 

> Declaration quotations are used for generating top-level declarations for constants, types, functions, instances etc. and use the syntax [d|declaration|]. Example: [d|x = 5 ; y = 1|] results in [ValD (VarP x0) (NormalB (LitE (IntegerL 5))) [], ValD (VarP y0) (NormalB (LitE (IntegerL 1))) []]. Note that the quotation can contain multiple declarations, so it evaluates to a list of declaration values.

#####Type
> [t|...|] "..." is a type, the quotation has type Q Type.

> Type quotations are used for generating type values, such as [t|Int|]

#####Pattern
> [p|...|] "..." is a pattern, the quotation has type Q Pat.

> Pattern quotations are used for generating patterns which are used, for example, in function declarations and case-expressions. [p|(x,y)|] generates the pattern TupP [VarP x,VarP y].

####Quasi Quotation
> quasi-quotation lets us build our own, custom quotations, but these are a more advanced topic that won't be covered in this post.

Quotations用来生成Haskell AST非常方便，同时，我们也可以定义自己的Quotation，这时就需要用到quasi-quotation了

###未完待续

------

**参考资料**

<a name="reference1" id="reference"></a><a name="reference2" id="reference"></a><a name="reference3" id="reference"></a>

1. [Template Haskell](https://wiki.haskell.org/Template_Haskell)
2. [Language.Haskell.TH](http://hackage.haskell.org/package/template-haskell)
3. [24 Days of GHC Extensions: Template Haskell](https://ocharles.org.uk/blog/guest-posts/2014-12-22-template-haskell.html)

------

**haskell学习总结**

* [开始学习Haskell](../2015-06-12/begin_haskell.html)
* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
