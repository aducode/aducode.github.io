<!--{layout:default title:在pyspark中操作hdfs文件}-->
## 背景
这段时间的工作主要是跟spark打交道，最近遇到类似这样的需求，统计一些数据（统计结果很小），然后直接把文本数据写入到hdfs文件中去。

之前一直使用的是scala语言，实现起来非常简单：

<pre class="language-scala line-numbers">
<code class="language-scala">
import org.apache.spark.SparkContext
import org.apache.hadoop.fs.{FileSystem, Path}

def path(filepath:String) =
  new Path(filepath)

def getFileSystem(sc:SparkContex) =
  FileSystem.get(sc.hadoopConfiguration)

def write(sc:SparkContext, filepath:String, content:String, overwrite:Boolean = true):Unit = {
  try{
    val fileSystem = getFileSystem(sc)
    val fileName = path(filepath)
    val out = fileSystem.create(fileName, overwrite)
    out.write(content.getBytes)
    out.flush
    out.close
  }catch{
    case e:Exception => System.err.println(e.toString)
  }
}</code>
</pre>

但是scala那陡峭的学习曲线，并不适合整个团队的发展，和业务的快速迭代，所以我们统一改成了spark的python接口：pyspark

那么pyspark中该如何直接操作hdfs上的文件呢？
找了一圈，并没有在python的SparkContext中找到hadoopConfiguration()方法，开始用了一些比较ugly的方法，比如在python中直接调用hadoop命令去操作文件。

后来通过看pyspark的代码，发现使用的是 **py4j** 来连接python与java，根据py4j的原理，可以通过以下代码在python中调用java对象来操作hdfs文件:

<pre class="language-python line-numbers">
<code class="language-python">
#!/usr/bin/python
# -*- coding:utf-8 -*-

def path(sc, filepath):
  """
  创建hadoop path对象
  :param sc sparkContext对象
  :param filename 文件绝对路径
  :return org.apache.hadoop.fs.Path对象
  """
  path_class = sc._gateway.jvm.org.apache.hadoop.fs.path
  return path_class(filepath)

def get_file_system(sc):
  """
  创建FileSystem
  :param sc SparkContext
  :return FileSystem对象
  """
  filesystem_class = sc._gateway.jvm.org.apache.hadoop.fs.FilFileSystem
  hadoop_configuration = sc._jsc.hadoopConfiguration()
  return filesystem_class.get(hadoop_configuration)

def write(sc, filepath, content, overwite=True):
  """
  写内容到hdfs文件
  :param sc SparkContext
  :param filepath 绝对路径
  :param content 文件内容
  :param overwrite 是否覆盖
  """
  try:
    filesystem = get_file_system(sc)
    out = filesystem.create(path(sc, filepath), overwrite)
    out.write(bytearray(content, "utf-8"))
    out.flush()
    out.close()
  except Error, e:
    print e
</code>
</pre>

那么这个神奇的py4j是什么呢？

可以看下官网的介绍：[http://www.py4j.org/](http://www.py4j.org/)

这里大概说下个人理解：
要想在java和python中使用这个东西，需要在java代码中开一个本地socket监听端口，并暴露一个entrypoint，python代码中通过JavaGateway来跟java进程交互，也就是说，这个是一个跨语言的RPC调用
