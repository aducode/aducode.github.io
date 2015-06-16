<!--{layout:default title:SpringMVC是如何查找方法的参数名的？}-->
#SpringMVC是如何查找方法的参数名的？
项目中用到SpringMVC，常见的用法像这样
<pre>
<code>
@Controller  
@RequestMapping("test")  
class Test{  
    @RequestMapping("/hello")  
    @ResponseBody  
    public Object test(@RequestParameter("name") String name){  
        return "hello! "+name;  
    }  
}
</code>
</pre>
当GET http://localhost:8080/test/hello?name=aducode请求到服务端时， SpringMVC的 DispatcherServlet处理请求，并根据URL找到@RequestMapping对应的方法，然后根据
@RequestParameter("name") 将url中的name值传递给方法调用
但是Spring还支持默认参数名
<pre>
<code>
@Controller  
@RequestMapping("test")  
class Test{  
    @RequestMapping("/hello")  
    @ResponseBody  
    public Object test(String name){  
        return "hello! "+name;  
    }  
}  
</code>
</pre>
即不适用@RequestParameter注解，昨天有人问我这种情况是如何找到url中对应参数的。考虑了一下，使用java的反射机制是不能获取参数名这样的信息的，于是大概查看了一下spring的源码，发现是使用了 org.springframework.core.LocalVariableTableParameterNameDiscoverer 这个类，原理就是读取class字节码，解析其中中的LocalVariableTable，得到方法的参数名称。这样的前提是java编译成class时，必须开启debug，如果关闭debug，就会失效。测试结果如下：

![img](http://aducode.github.io/images/2015-06-16/20140821162952784.jpg "去掉debug")