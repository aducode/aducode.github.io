<!--{layout:default title:利用CROS跨域}-->

CROS全称：Cross-Origin Resource Sharing
主要用于不同domain下js进行互操作，目前浏览器的支持情况如下：

![img](../../images/2015-08-07/cros.png)

###服务端
要使用CROS需要在服务端设置http header，这里以Java Servlet为例：
<pre class="language-java line-number">
<code>
response.setHeader("Access-Control-Allow-Origin", "http://www.xxx.com");
</code>
</pre>

当然也可以直接在nginx里设置:
<pre class="language-c line-number">
<code>
server {
	add_header Access-Control-Allow-Origin *;
}
</code>
</pre>
当然上面的做法比较危险

###客户端
客户端端就是指不同的浏览器了，根据上面的图我们可以看到比较新的浏览器都是支持CROS,利用JQuery就可以方便的发送跨域请求了
<pre class="language-javascript line-number">
<code>
$.ajax({
	async: true,
	url: 'http://www.xxx.com',
	data: 'xxxxx',
	type: 'POST',
	dataType: 'json',
	contentType: "application/x-www-form-urlencoded; charset=UTF-8",
	success: function(data) {
		alert('data from http server:' + data)
	},
	error: function(a, b, c, d){
		alert("some error")
	}
})
</code>
</pre>
但是注意IE8 IE9是part support的。。在IE8 9下使用上面代码是有问题的，详见[Stack Overflow](http://stackoverflow.com/questions/10232017/ie9-jquery-ajax-with-cors-returns-access-is-denied)
其实是IE8 IE9跨域不是使用XmlHttpRequest对象，而是使用IE特有的(IE10以后基本符合w3c标准了)XDomainRequest：
<pre class="language-javascript line-number">
<code>
if ( window.XDomainRequest ) { //判断是否存在XDomainRequest 
	var xdr
	var data=''
	var first = true
	for(var name in params){
	if(!first){
		data += '&'
	}
	first = false
		data += encodeURIComponent(name) + '=' + encodeURIComponent(params[name]) //这里将数据作为query string参数传给服务器
	}
	xdr = new XDomainRequest()
	if(xdr){
		xdr.onprogress = function(){
		//开始接收数据
		//alert(xdr.responseText)
		}
		xdr.onload = function(){
			//数据完全返回  相当于success
			alert(xdr.responseText)
		}
		xdr.ontimeout = function(){
			//超时
			alert("网络异常，请稍后再试");
		}
		xdr.onerror = function(){
			//on error
			alert("网络异常，请稍后再试");;
		}
		xdr.timeout = 10000
		xdr.open('POST', url+'?'+data)
		xdr.send()   //xdr.send(data) //当然也可以放到请求体内
	} else {
		alert('new xdr fail')
	}
}
</code>
</pre>