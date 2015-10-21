<!--{layout:default title:haskell学习总结(四)::强大的Parsec}-->

上一篇稍微总结了一下haskell中的正则表达式的用法，正则表达式已经很强大了，基本满足大部分的文本处理需求了，但是如果遇到非常变态的文本处理，比如自己实现一门DSL，那么正则自能用来做词法分析，语法分析就需要用到今天主角:Parsec了。

####一. Parsec学习资料:

* [http://hackage.haskell.org/package/parsec](http://hackage.haskell.org/package/parsec) parsec API文档
* [https://wiki.haskell.org/Parsec](https://wiki.haskell.org/Parsec)
* [http://research.microsoft.com/en-us/um/people/daan/download/parsec/parsec.pdf](http://research.microsoft.com/en-us/um/people/daan/download/parsec/parsec.pdf) 这篇文章有些parsec高级用法

####二. Parser基本的连接符

Parser这个Monad是Parsec中最简单，最常用的，Monad相当于一个盒子，我们把感兴趣的类型数据放进盒子里，在解析的过程中盒子内进行字符流的输入/移动/判断等操作，这些操作对我们来说是透明的。

Parser有两个非常重要的操作(&lt;|&gt;)和(&gt;&gt;= 也可以用do block)

* &lt;|&gt;
	
	这个二元操作符类似或的操作 parser1 &lt;|&gt; parser2 当第一个parser1解析失败的时候，就会解析parser2;

	需要注意的一点是如果parser1匹配多个字符，并且失败的话，并不会回退，如果想回退到解析前的状态开始解析parser2，可以在parser1前面加上try: 
	
	(try parser1)&lt;|&gt;parser2

* &gt;&gt;=或者do block
	
	类似与的操作 parser1&gt;&gt;=parser2 当parser1和parser2同时解析成功的时候，才算成功，并且返回parser2的值；
	
	当然如果要返回parser1的值，或者parser1与parser2操作后的值，可以用do block: 
	
	do {p1&lt;-parser1;p2&lt;-parser2;return p1++p2;}

<pre class="language-haskell number-lines">
<code>
-- symbol表示abc或者123
symbol::Parser String
symbol = do
	section1<-try $ string "abc" &lt;|&gt; string "123"
	section2<-string ",Hi"
	return $ section1++section2
	
parse symbol "" "123,Hi"
-- Right "123,Hi"
parse symbol "" "abc,Hi"
-- Right "abc,Hi"
parse symbol "" "234"
-- Left (line 1, column 1):
-- unexcepted "2"
-- excepting "abc" or "123"
parse symbol "" "123"
-- Left (line 1, column 4)
-- unexcepted end of input
-- excepting ",Hi"
</code>
</pre>

####三.用Parsec解析语言

定义关键词

<pre class="language-haskell number-lines">
<code>
-- 首先定义一些关键词for where if else 
-- 还有表示类型的关键词
keywordFor::Parser String
keywordFor = try $ do
	s<-string "for"
	notFollowedBy (alphaNum<|>char '_')
	return s

keywordWhere::Parser String
keywordWhere = try $ do
	s<-string "where"
	notFollowedBy (alphaNum<|>char '_')
	return s

keywordIf::Parser String
keywordIf = try $ do
	s<-string "if"
	notFollowedBy (alphaNum<|>char '_')
	return s
keywordElse::Parser String
keywordElse = try $ do
	s<-string "else"
	notFollowedBy (alphaNum<|>char '_')
	return s
	
theType::Parser String
theType = do
	s<-string "int" <|> string "char" <|> string "string"
	notFollowedBy (alphaNum<|> char '_')
	return s
</code>
</pre>

定义因子(是参与* /运算)

<pre class="language-haskell number-lines">
<code>
-- FACTOR
-- 因子可以是整数/字符/字符串/变量
factor::Parser String
factor = do 
		di<-many1 digit
		return di
	<|> do
		ch<-between (char '\'') (char '\'') (noneOf "'")
		return $ '\'':ch:'\'':[]
	<|> do
		s<-between (char '"') (char '"') (many (noneOf "\""))
		return $ "\"" ++ s ++ "\""
	<|> var
	<|> do
		-- 引子可能是括号内的表达式
		-- expression一会儿说明
		e<-between ((char '(') >> spaces) (spaces>>(char ')')) expression
		return $ "("++e++")"
		
-- 变量名不包括关键字
-- 变量名以字母或下划线开头，可以包括字母 数字 和下划线
var::Parser String
var = do
		notFollowedBy keywordIf
		notFollowedBy keywordElse
		notFollowedBy keywordWhere
		notFollowedBy keywordFor
		
		notFollowedBy theType
		fst<-letter<|> char '_'
		rst<-many (alphaNum<|> char '_')
		return $ fst:rst
</code>
</pre>


接下来是解析* /运算

term的定义需要消除左递归

<pre class="language-haskell number-lines">
<code>
-- TERM
term::Parser String
term = do
		f<-factor
		spaces	
		t<-option "" term'
		return $ f++t
		
term'::Parser String
term' = do
		op<-(try $ string "*")<|>(try $ string "/")
		spaces
		f<-factor
		t'<-option "" term'
		return $ op++f++t'
</code>
</pre>

再接下来是低优先级的+ -运算，同样要消除左递归

<pre class="language-haskell number-lines">
<code>
plus::Parser String
plus = do
		t<-term
		p<-option "" plus'
		return $ t++p
		
plus'::Parser String
plus' = do
		op<-(string "+")<|>(string "-")
		spaces
		t<-term
		p'<- option "" plus'
		return $ op++t++p'
</code>
</pre>

再接下来是逻辑运算

<pre class="language-haskell number-lines">
<code>
bool::Parser String
bool = do
	p<-plus
	b'<-option "" bool'
	return $ p++b'

bool'::Parser String
bool' = do
	op<-(try $ string "==")
		<|> (try $ string "!=")
		<|> (try $ string ">=")
		<|> (try $ string "<=")
		<|> (try $ string ">")
		<|> (try $ string "<")
	spaces
	p<-plus
	b'<-option "" bool'
	return $ op++p++b'
</code>
</pre>

然后是赋值符号(=)

<pre class="language-haskell number-lines">
<code>

--EXPRESSION
expression::Parser String
expression = do
	b<-bool
	e'<-option "" expression'
	return $ b++e'
	
expression'::Parser String
expression' = do
	op<-string "="
	spaces
	b<-bool
	e'<-option "" expression'
	return $ op++b++e'
</code>
</pre>

至此表达式解析就完成了，我们可以更进一步的解析语句了,其中一条最基本的语句是expression+";"

或者是一个语句块block

复杂一点再加上控制结构(if else/where/for)

<pre class="language-haskell number-lines">
<code>
-- STATEMENT
statement::Parser String
statement = do
			spaces
			i<-try ifstatement
			spaces
			return i
		<|> do
			spaces
			w<-try wherestatement
			spaces
			return w
		<|> do
			spaces
			f<-try forstatement
			spaces
			return f
		<|> do
			spaces
			b<-try block
			spaces
			return b
		<|> do
			spaces
			d<-try dec
			spaces
			char ';'<|> newline
			spaces
			return $ d++";"
		<|> do
			spaces
			e<-try expression
			spaces
			char ';' <|> newline
			spaces
			return $ e++";"

dec::Parser String
dec = do
			t<-theType
			spaces
			v<-var
			e'<-option "" expression'
			return $ t++ " " ++ v++e'

--FOR
forstatement::Parser String
forstatement = do
			string "for"
			spaces
			char '('
			spaces
			e1<-expression
			spaces
			char ';'
			spaces
			e2<-expression
			spaces
			char ';'
			spaces
			e3<-expression
			char ')'
			spaces
			b1<-block
			return $ "FOR("++e1++";"++e2++";"++e3++")"++b1
--WHERE
wherestatement::Parser String
wherestatement = do
			string "where"
			spaces
			e1<-between (char '(') (char ')') expression
			spaces
			b1<-block
			return $ "WHERE("++e1++")"++b1
--IF
ifstatement::Parser String
ifstatement = do
			string "if"
			spaces
			e1<-  between (char '(') (char ')') expression --expression
			spaces
			b1<- block
			return $ "IF("++e1++")"++b1
--BLOCK
block::Parser String
block = do
	statements<-between (char '{') (char '}') (many statement)
	return $ "{"++ (conncat statements) ++"}"
</code>
</pre>

最后设置一个入口

<pre class="language-haskell number-lines">
<code>
-- ATOM
atom::Parser String
atom = do
	s<-statement
	s'<-option "" atom
	return $ s++s'
</code>
</pre>

这样就完成了

<pre class="language-haskell number-lines">
<code>
parse atom "ATOM" "int a;char b='a';for(a=0;a<26;a=a+1){b=b+1;}"
-- Right "int a;char b='a';FOR(a=0;a<26;a=a+1){b=b+1;}"
</code>
</pre>

当然以上的例子比较简单，在解析文本的时候没做过多的处理，只是原样输出字符串

------

**haskell学习总结**

* [开始学习Haskell](../2015-06-12/begin_haskell.html)
* [haskell学习总结(一)::初级篇](../2015-07-02/learn_haskell_lession1.html)
* [haskell学习总结(二)::元编程](../2015-08-12/learn_haskell_lession2.html)
* [haskell学习总结(三)::正则表达式](../2015-10-13/learn_haskell_lession3.html)
* [haskell学习总结(四)::强大的Parsec](../2015-10-21/learn_haskell_lession4.html)