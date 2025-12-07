## 漏洞扫描

### 流程

1.主机发现

2.端口扫描

3.基于指针发现目标系统

4.发现服务，banner，服务行为，文件发现

5.特征匹配，发现漏洞

## NESSUS



## NMap

NSE(Nmap Scripting Engine) Lua语言

nmap不是一个完整的漏扫软件

vuln、exploit两种类型有重叠。

脚本进一步细分，safe，intrusive

/usr/share/nmap/scripts/script.db包含所有脚本的索引和分类

cat script.db | grep 'vuln\exploit'





sudo nmap --script vuln x.x.x.x

