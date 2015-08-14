<!--{layout:default title:haskell学习总结(二)::元编程}-->
上一篇总结了一下haskell中的基本语法，这篇打算总结一下haskell中的**元编程:**TemplateHaskell<sup>[[1]](#reference1)</sup><sup>[[2]](#reference2)</sup><sup>[[3]](#reference3)</sup>
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
printf format = lamE (args fmt) (body fmt)
    where fmt = tokenize format
</code>
</pre>

###未完待续

------

**参考资料**

<a name="reference1" id="reference"></a><a name="reference2" id="reference"></a><a name="reference3" id="reference"></a>

1. [Template Haskell](https://wiki.haskell.org/Template_Haskell)
2. [Language.Haskell.TH](http://hackage.haskell.org/package/template-haskell-2.9.0.0/docs/Language-Haskell-TH.html)
3. [24 Days of GHC Extensions: Template Haskell](https://ocharles.org.uk/blog/guest-posts/2014-12-22-template-haskell.html)

------

**haskell学习总结**

* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
