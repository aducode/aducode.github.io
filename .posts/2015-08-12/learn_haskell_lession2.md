<!--{layout:default title:haskell学习总结(二)::元编程}-->
上一篇总结了一下haskell中的基本语法，这篇打算总结一下haskell中的**元编程:**TemplateHaskell<sup>[[1]](#reference1)</sup><sup>[[2]](#reference2)</sup><sup>[[3]](#reference3)</sup><sup>[[4]](#reference4)</sup>

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

-- Quotation相关的函数必须放在单独的一个文件内

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

注意事项：

<pre class="language-haskell line-numbers">
<code>
{-# LANGUAGE TemplateHaskell #-}
module FstN where
import Language.Haskell.TH

fstN::Int->ExpQ
fstN n =let x=mkName "x" in
        lamE [tupP (varP x: replicate (n-1) wildP)] (varE x)

fstN'::Int->Q Exp
fstN' n = do
        x<-newName "x"
        return $ LamE [TupP (VarP x: replicate (n-1) WildP)] (VarE x)

-- 这样写是错误的
-- main方法与fstN不能在同一个Module下面
-- main::IO ()
-- main = do
--         print $ $(fstN 3) ("hello world", 1,2)
</code>
</pre>

> An important restriction on Template Haskell to remember is when inside a splice you can only call functions defined in imported modules, not functions defined elsewhere in the same module. Quotations and splice have to be defined in separate modules, otherwise you’ll see this error:

> GHC stage restriction:
  `...' is used in a top-level splice or annotation,
  and must be imported, not defined locally
  

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


####使用QuasiQuote修改我们的PrintF

* QuasiQuoter之quoteExp

<pre class="language-haskell line-numbers">
<code>
-- PrintF.hs
{-# LANGUAGE TemplateHaskell #-}
module PrintF where

import Language.Haskell.TH
import Language.Haskell.TH.Quote

-- printf函数同上
printf::String->Q Exp
printf = ...

-- QuasiQuoter

pf = QuasiQuoter {
		quoteExp = printf				-- 这里使用上面的printf函数
		, quotePat = undefined			-- 其余的首先忽略
		, quoteType = undefined
		, quoteDec = undefined
	}
	
-- Main.hs
-- 下面是修改后的Main.hs

{-# LANGUAGE TemplateHaskell #-}
-- 要使用自定义的QuasiQuoter，那么必须加上下面的扩展
{-# LANGUAGE QuasiQuotes 	 #-}
module Main where
import PrintF (pf)
-- import Language.Haskell.TH.Quote

main::IO ()
main = do
	-- 如要使用下面的方法，需要import Language.Haskell.TH.Quote
	-- putStrLn $ $(quoteExp pf "hello,%s\nthe Answer to Life, the Universe and Everthing is %d") "Issac" 42
	
	-- [pf| |]之中的结果已经是一个lambda了，不要再用$()了
	putStrLn $ [pf|hello,%s\nthe Answer to Life, the Universe and Everthing is %d|] "Issac" 42

</code>
</pre>

* QuasiQuoter之quotePat

<pre class="language-haskell line-numbers">
<code>
--PrintF.hs

genPat::String -> Q Pat
--genPat str = return $ VarP $ mkName str
genPat str = do
	nm <- newName str
	return $ VarP nm


pf = QuasiQuoter {
		quoteExp = printf				-- 这里使用上面的printf函数
		, quotePat = genPat				-- 指定genPat函数		
		, quoteType = undefined			-- 其余的首先忽略
		, quoteDec = undefined
	}
	
-- Main.hs

-- 这里使用的就是pf quasi-quoter的quotePat
-- 相当于
--	test x = x + 1
-- 可见这个位置的[pf||]内容会被当成函数pattern使用
test [pf|x|] = x + 1

</code>
</pre>

###未完待续

------

**参考资料**

<a name="reference1" id="reference1"></a><a name="reference2" id="reference2"></a><a name="reference3" id="reference3"></a><a name="reference4" id="reference4"></a>

1. [Template Haskell](https://wiki.haskell.org/Template_Haskell)
2. [Language.Haskell.TH](http://hackage.haskell.org/package/template-haskell)
3. [24 Days of GHC Extensions: Template Haskell](https://ocharles.org.uk/blog/guest-posts/2014-12-22-template-haskell.html)
4. [Template Meta-programming for Haskell[PDF]](http://research.microsoft.com/pubs/67015/meta-haskell.pdf)

------

**haskell学习总结**

* [开始学习Haskell](../2015-06-12/begin_haskell.html)
* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
* [haskell学习总结(三)::正则表达式](../2015-10-13/learn_haskell_lession3.html)
* [haskell学习总结(四)::强大的Parsec](../2015-10-21/learn_haskell_lession4.html)
