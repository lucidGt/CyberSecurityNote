## BASH环境相关

Linux kernel<->Shell(解析命令)<->Terminal

常用Shell:bash、zsh、fish

获取shell环境: echo $SHELL  echo->/usr/bin/xx

### 1.Bash环境变量(environment)

#### 1.(定义局部环境变量)

1.定义 b=xxx

#### 2.(定义全局环境变量)（能够被子进程继承）

1.定义 export b=xxx

2.进入子shell进程命令:bash

#### 3.查询变量相关

1.查询环境变量:env

2.查看指定环境变量:echo $symbol

#### 4.历史命令相关 

敏感信息路径:/etc/environment、/etc/profile、etc/zsh/zshenv

保存路径:~/.bash_history

配置历史数据容量:

设置缓存中保存历史命令的数量：$HISTSIZE =xx 

设置文件中保存历史命令的数量：$HISTFILESIZE=xx  

## 管道 & 重定向

### 管道

管道的机制，把一个数据的输出作为另一个程序的输入，两个命令直接通过“|”连接。

命令行程序三个数据流

1.标准输入 (STDIN - 0)输入数据 、

2.标准输出(STDOUT - 1)输出数据（默认当前终端）

3.标准报错(STDERR - 2)输出数据（默认当前终端）

### 重定向

重定向标准错误到标准输出 

2>&1

nc -z 127.0.0.1 1-1200  2>&1 | awk  "/ open/"

#### 重定向符号

标准输入符号 0>

标准输出符号 1>，>(默认)

报错输出符号 2>

| 隧道只能单向传输数据

#### 重定向覆盖文件

echo "xxx" > 文件名

#### 重定向追加到已有文件

echo "xxx" >> 文件名

#### 从文件重定向

wc -mw <  xx.txt

