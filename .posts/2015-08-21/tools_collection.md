<!--{layout:default title:收集有用的软件}-->

这里记录一下收藏的有用的软件

###1. Lantern

> 主要目的是访问：得到快速可靠的连接，拥抱广阔的因特网，自由浏览。绝大多数翻墙软件需要服务器。在Lantern系统中，每台机器都可以作为服务器，从而比其他工 具提供更多的容量。通过运行Lantern，每个在非封锁区的电脑，都可以变成封锁区用户的代理，使他们可以访问被封锁的网站，诸如 Twitter，Facebook，Youtube，等等。Lantern的核心是信任网络，使用者邀请他们的朋友来建立Lantern网络（使用最新版的Lantern当前为1.4无需邀请直接使用）。通过只邀请他们信任的人分享因特网连接，大家共同努力，来增加网络反抗审查者的封锁的能力。你的Lantern朋友越多，因特网的速度和可靠性就越高。工作原理如下图：
> ![img](../../images/2015-08-21/lantern.gif)

* [Github:Lantern](https://github.com/getlantern/lantern)
* [教程](http://www.cooear.com/archives/239.htm)

用来翻墙的，只要安装chrome浏览器，无需配置，直接使用!


###2. ttygif

* [Github:ttygif](https://github.com/icholy/ttygif)

一款console录屏软件

###3. graphviz

* [Github:graphviz](https://github.com/ellson/graphviz)
* [官网](http://www.graphviz.org/)

画图软件，我的[regularpy](https://github.com/aducode/regularpy)项目里面有用到，画些简单的图还是很好用的

###4. Google-IPs

* [Github:Google-IPs](https://github.com/Playkid/Google-IPs)

Google全球IP地址库

###5. SAO Utils

* [SAO Utils](http://www.gpbeta.com/post/develop/sao-utils/)

能让你的windows桌面变成[《刀剑神域》](http://baike.baidu.com/link?url=WIE9MRV_x1KBNX0e5IxaFq0AI7_iKA34BHKrc96w4Iwkk64rbhZLsfssFWl7BInjcmIraKA-xGrXlbfx58E4iuVouTsv1tqGzw9NfAk4Iym), 适合像我这样的中二病宅男XD

###6. 修改java字节码

* [Github:javassist](https://github.com/jboss-javassist/javassist)
* [ASM](http://asm.ow2.org/)

若要修改java字节码(class)文件，有好多种方法:

1. 学习jvm字节码规范，了解class文件格式，手动修改，当然这个难度太大，并且不利于批量/实时操作；
2. 使用Javassist，它支持java源码级别操作，即使一点也不了解字节码规范，也能轻松上手，缺点是速度比不上ASM（毕竟插入的是java源码，还需要经过编译阶段）；
3. 使用ASM框架，支持字节码指令集级别的操作，使用起来比较麻烦，比如要Object [][]类型在ASM中要写成 [[Ljava/lang/Object, 但是速度比Javassist快，毕竟spring的AOP就用的是ASM的封装：cglib；

###7. 根据数据库table生成javabean的eclipse插件

* [参考资料](http://blog.csdn.net/z1721940401/article/details/24836931)
* [点此下载](../../attachments/2015-09-16/JavaBeanTool_1.0.0.201112040957.rar)

###8. 很好的在线IDE
* [主页](http://www.tutorialspoint.com/)
* [c++11](http://www.tutorialspoint.com/compile_cpp11_online.php)
* [java](http://www.tutorialspoint.com/compile_java_online.php)

