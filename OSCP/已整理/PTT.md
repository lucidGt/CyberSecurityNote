# PTT（Pass The Ticket）

## 介绍

PTT=Pass The Ticket 传票据攻击

常见PTT是使用kerberos票据（Ticket）进行验证，不需要密码，也不需要NTLM hash。

## PTT和PTH区别

| 对比     | PTH           | PTT                     |
| -------- | ------------- | ----------------------- |
|          | Pass-The-Hash | Pass-The-Ticket         |
| 用的东西 | NTLM hash     | Kerberos票据（TGT/TGS） |
| 协议     | NTLM          | Kerberos                |
| 常见服务 | SMB/WINRM/WMI | SMB/LDAP/HTTP/CIFS      |
| 频率     | 高            | 中（AD场景）            |

## 什么是Kerberos票据？

在AD里，Kerberos登录大致是

1.用户登录->拿到TGT票据

2.访问某个服务->换TGS票据

3.用票据访问服务

PTT做的事就是

我直接把“已经拿到的票据’塞到会话里

## PTT能干嘛？

1）访问SMB（用Kerberos）

2）访问LDAP

3）横向到其他机器

4）打DC（票据权限足够）

全程不需要密码，也不需要Hash

## 利用方式

有HASH->想PTH(SMB)

有票据->想PTT（kerberos）

有密码->想RDP/WINRM

