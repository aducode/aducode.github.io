<!--{layout:default title:Java MessageFormat的坑}-->

今天在使用Java的MessageFormat类的时候遇到一个坑，在此记录一下。

在项目中使用Mybatis批量插入的时候用到了MessageForamt，代码如下：
<pre class="language-java line-numbers">
<code>
/**
 * Person类
 */
public class Person{
	private String name;
	private int age;
	
	public void setName(String name){
		this.name = name;
	}
	public String getName(){
		return this.name;
	}
	
	public void setAge(int age){
		this.age = age;
	}
	public int getAge(){
		return this.age;
	}
}

/**
 * Person Dao 接口
 * 使用mybatis的注解方式
 */
public interface PersonDao{
	/**
	 * 单条插入语句
	 * @param person待插入的bean
	 */
	@Insert("insert into t_person (name, age) values (#{person.name}, #{person.age})")
	int insert(@Param("person") Person person);
	
	/**
	 * 批量插入接口
	 * @param person 待插入的数据列表
	 * @return 插入条数
	 */
	@InsertProvider(type=PersonSQLProvider.class, method="provideInsertSQL")
	int batchInsert(@Param("person")List<Person> person);
	
	/**
	 * Provedier类，上面的插入接口注解使用
	 */
	static class PersonSQLProvider{
		/**
		 * 上面插入接口注解中指定的方法
		 * @param params 上面批量插入接口中的参数会转换成map传过来
		 *	 params {"person"=List<Person>}
		 * @return 返回mybatis注解中的sql语句
		 */
		public String providerInsertSQL(Map<String, Object> params){
			//获取插入列表
			List<Person> personList = params.get("person");
			StringBuilder sb = new StringBuilder();
			sb.append("insert into t_person (name, age) values ");
			//MessageFormat格式化中要使用{0}表示格式化的第一个参数
			//所以下面最外层的{}要写成'{''}',否则MessageFormat会找不到真正的格式化参数{0}
			MessageFormat mf = new MessageFormat("(#'{'person[{0}].name'}', #'{'person[{0}].age'}')");
			for(int i=0;i&lt;personList.size();i++){
				if(i!=0){
					sb.append(",");
				}
				//我们的目标是生成mybatis使用的语句，比如列表size=2，那么用最后的结果是：
				//	insert into t_person (name, age) values (#{person[0].name}, #{person[0].age}), (#{person[1].name}, #{person[0].age})
				//开始测试的时候以下写法没有任何问题，但是当批量插入的条数大于1000的时候就会出错
				//原来MessageFormat.format()参数是整形的时候，比如1000，那么格式化后的结果是：
				//			1,000			//多了个用于每三位分隔的逗号，导致mybatis解析出错
				//sb.append(mf.format(new Integer[]{i}));
				//所以应该改成下面的写法，以String的类型进行格式化，就不会多那个分隔符","
				sb.append(mf.format(new String[]{String.valueOf(i)}));
			}
			return sb.toString();
		}
	}
}
</code>
</pre>


教训就是：

MessageFormat.format()参数是整形的时候，比如1000，那么格式化后的结果是：1,000。多了个用于每三位分隔的逗号，导致mybatis解析出错
所以遇到这种情况，应该以String类型进行格式化:)