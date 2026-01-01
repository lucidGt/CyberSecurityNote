## bash脚本

The GNU Borune-Again Shell (Bash) 脚本引擎，自动化任务和过程



### 执行bash脚本

拓展名为 .sh

起始语句 !/bin/bash

脚本需要可执行权限 x

chmod+x <fileName>.sh

./<fileName>.sh

### 变量

user1 = $(whoami)

user2 = 'whoami'

va1=value1

echo $var1

var=vulue2

echo $var2

$(var1=newvar1)

echo $var1

###  参数

$0	脚本文件名自己

$1-$9 Bash的前9个参数

$#	传递bash参数是数量

$@	传递bash脚本的所有参数

$?	最近运行的程序的退出状态

$USER	运行脚本的用户的用户名

$HOSTNAME	计算名的主机名

$RANDOM	生成一个随机数

$LINENO	脚本中的当前行号

