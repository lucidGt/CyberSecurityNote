## Dns(Domain Name System) 是一个层级分布式数据库

### DNS工作过程

DNS服务器缓存，操作系统缓存，游览器等应用程序有独立缓存

DNS权限服务器控制缓存TTL

DNS是主动信息收集最有价值的服务类型

DNS记录类型

### DNS记录类型

NS	包含承载域DNS记录授权服务器的名称

A	包含主机名的IP地址

MX	包含负责处理该域电子邮件的服务器的名称，可以有多个MX记录

PTR	指针记录（反向区域使用）

CNAME	别名记录，指向其他主机记录

TXT	文本记录，可以包含任意消息，常用于域所有权验证

### 查询记录

host <domain> 查A记录

host -t mx <domain> 查看MX记录

host -t txt <domain> 查看TXT记录

DNS正向查询

for dy in $(cat xx.txt); do host $dy.<domian>; done

不存在返回（NXDOMAIN)

### 安装字典

sudo apt install seclists

### DNS逆向破解

for ip in $(seq 50-100);do host xxx.xxx.xxx.$ip; done | grep -v 'not found'

### 区域传输

同一区域中域名服务器间的数据库复制 master->slave (TCP 53)

管理员配置错误，允许所有人进行执行区域复制

1.先发现目标域的NS记录

host -t ns <domain> | cut -d " " -f 4

2.尝试区域传输

host -l <domain> ns1.<domain>

DNS自动枚举工具 (Dnsrecon)

dnsrecon -d <domain> -t axfr

dnsrecon -d <domain> -D <file> -t brt

dnsrecon -bykwsad <domain>

dnsenum <domain> -f list.txt

## TCP、UDP端口扫描

### 通过Netcat扫描TCP、UDP

#### SYN扫描

NMAP默认使用，不完成三次握手，信息未到达应用层，不产生应用层日志（网络层检测），快速

sudo nmap -sS <ip>

#### TCP全连接扫描

当用户没有Raw socket权限时，默认使用Berkeley sockets Api,默认使用全TCP扫描

sudo nmap -sT <ip>

#### UDP扫描

nmap使用两种方法进行UDP端口扫描，ICMP Port unreachable 和 协议指令（SNMP)

需要Sudo权限

sudo namp -sU <ip>

nc -nvv -w 1 -z <ip> <port> 抓包分析TCP三次握手

UDP是无状态尽力传输协议，没有三次握手机制，使用针对协议的UDP提高准确度

nc -nvv -w 1 -z -u <ip> <port>

