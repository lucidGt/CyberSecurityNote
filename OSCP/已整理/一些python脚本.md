## Responder

介绍：名称解析投毒（LLMNER/NBS/mDNS）+ 假服务端（SMB/HTTP等）组合工具，在观察捕获NTLM认证流量。

### 查看那些网卡

ip a

（1）lo 本地回环

（2）eth0 真实物理网卡

（3）tun0 VPN隧道

ip route get <targetIp>

### 监听

sudo python3 Responder.py -I tun0

### 分析模式

sudo python3 Responder.py -I tun0 -A

（1）那台主机在问某个主机名

（2）什么时候触发

（3）是否值得继续

### 常用开关

Responder.conf控制

那些Poisoners（LLMNR/NBNS/mDNS）

那些Servers（SMB/HTTP/HTTPS/FTP/LDAP/MSSQL）

先-A观察

再去Responder.conf设置开的模块

### 抓到的东西怎么分析

（1）抓到的一般都是一次性握手材料（Net-NTLMv2）不就是NTLM hash本体

（2）用途：离线口令猜测

