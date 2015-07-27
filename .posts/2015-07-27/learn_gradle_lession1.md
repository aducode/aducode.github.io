<!--{layout:default title:学习使用Gradle}-->
构建Java项目使用什么？

1. [Ant](http://ant.apache.org/), 比较老了，个人用的不多，但是给我的感觉是用起来很灵活，没那么多条条框框，想怎么扩展怎么扩展
2. [Maven](http://maven.apache.org/) 绝对是目前使用最多的：Repository Centre，依赖管理，使用起来也很方便，但是要扩展的时候就稍微有些麻烦
3. [Gradle](http://gradle.org/)  比较新的东西，结合了Ant和Maven的优点，所以我打算好好学习学习；做技术的也要与时俱进嘛，新的技术能够出现就一定有比旧技术先进的地方:)

> Gradle 是以 Groovy 语言为基础，面向Java应用为主。基于DSL（领域特定语言）语法的自动化构建工具。

##安装
目前最新版2.5,下载地址:[https://services.gradle.org/distributions/gradle-2.5-all.zip](https://services.gradle.org/distributions/gradle-2.5-all.zip)
解压，配置环境变量，gradle -v 成功搞定！

##创建基于Gradle的Java项目
用过Maven都知道，可以使用maven命令直接创建出项目的目录结构，但是gradle不像maven那样有固定的项目结构，gradle原生API是不支持的，要想做到这一点，我们可以自定义一个task。
创建一个目录，作为项目的根目录，然后新建一个build.gradle文件：
<pre class="language-bash line-number">
<code>
//build.gradle
apply plugin: 'java'    //使用java插件，默认提供build等task
task 'initproject' << { //自定义的task
	sourceSets*.java.srcDirs*.each{it.mkdirs()}
	sourceSets*.resource.srcDirs*.each{it.mkdirs()}
}
</code>
</pre>

随后使用命令：gradle initproject，即可创建好和Maven项目一致的目录结构了

-----
未完待续
