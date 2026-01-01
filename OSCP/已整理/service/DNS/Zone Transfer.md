# Zone Transfer

## 介绍

Zone Transfer = DNS服务器之间同步整个域名数据库的机制

本来DNS主从服务器来同步记录的正常功能，但如果配置不当，任何人都能把整个域信息拉走。

## DNS ZONE是什么？

一个ZONE（区域）本质上是一个域名数据库，里面包括：

1）主机名->IP

2）子域名

3）邮件服务器（MX）

4）NS记录

6）内部服务器名（常常非常敏感）

例如：example.com的zone里面可能有：

www.example.com

dev.example.com

mail.example.com

## Zone Transfer正常工作原理

Primary DNS（主）  →  Secondary DNS（从）
        |
        |  AXFR / IXFR
        |
        ↓

正常流程

1）主DNS负责写入/修改记录

2）从DNS定期向主DNS请求同步

3）同步方式

​	AXFR：全量同步（整个ZONE)

​	IXFR：增量同步（只同步变化）

关键点：主DNS应该只允许可信的从DNSIP做ZONE Transfer

## 漏洞从哪里来？

主DNS被配置成：

allow-transfer{any;};

或者允许所有IP AXFR

结果：

攻击者可以伪装成从DNS，向主DNS请求DNS数据库。

## 攻击者视角：ZONE Transfer到底在干嘛？

正常DNS枚举

dig www.example.com

只能一个一个问

Zone Transfer

dig axfr example.com @DNS_IP

直接拿走整个域

可能得到：

1）内部主机名

2）AD域控（dc01/dc02）

3）VPN/DEV/TEST主机

4）内网IP段

5）邮件服务器

6）命名规则（user-pc01/sql-prod01）

## AXFR和IXFR区别

| 类型 | 含义         | 攻击常用 |
| ---- | ------------ | -------- |
| AXFR | 全量区域传送 | 最重要   |
| IXFR | 增量区域传送 | 不常用   |

A = All（全部）

I = Incremental（增量）

XFR = Transfer

AXFR = All + Transfer

IXFR = Incremental + Transfer

## 使用

nmap -p 53 targetIp

dig axfr example.com @targetIp

dnsrecon -d example.com -t axfr