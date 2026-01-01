# impacket-lookupsid

## 介绍

impacket-lookupsid是通过MSRPC/LSA（以及SAMR等相关接口）去“枚举/解析Windows的SID",从而得到域或主机上的用户、组等对象名称。

常见场景是拿到一个可用的账号（或某些情况下匿名/低权限也行）

然后用它去把一段RID范围跑一遍，找出那些SID存在，进而推断出那些用户/组。

（这类行为也称为RID cycling/SIB bruteForce)

你经常会看到它用于：

（1）域用户/组枚举：找出Domain admins、普通用户、服务账号等

（2）确认账号/组是否存在：通过SID<->名称映射结果判断

（3）渗透测试信息收集

## 前提条件

### 1）前置服务

（1）TCP 445

​	（1）工具通过SMB->MSRPC（LSARPC/SAMR）来查询SID

（2）TCP 139

​	老版本Windows

impacket-lookupsid关键看445端口通不通

### 2）再看SMB是否可访问

smbclient -L <targetIp> -N

能返回共享列表/提示匿名限制不报错

### 3）是否需要账号？（匿名VS凭据）

（1）匿名A

impacket-lookupsid <targetIp>

impacket-lockupsid anonymous@manager.htb -no-pass

（2）已有账号

impacket-lookupsid domain/username:password@<targetIp>

### 4）结果

显示Domain SID + 一堆用户名/组名

## 为什么anonymous可用使用呢？

1）允许“空会话/Null Session”连SMB/RPC

匿名先要通过SMB(445)建立会话，然后再走MSRPC（LSA/SAMR）去查SID

如果目标允许匿名建立这种会话，就能连上发起RPC请求

2）LSA/SAMR对匿名开放了“查名/查SID”的权限

lookupsid做的事本质是：

（1）拿到域/主机的DomainSID

（2）然后用RID递增去问：“这个SID存在吗？对应什么用户名/组名”

如果目标没有把SID<->Name的解析权限收紧，匿名就能得到结果

3）“EveryOne”包含了anonymous

有些环境位了兼容旧系统，会启用类似策略，使得ACL判断力Everyone也包含了anonymous,这会让匿名在一些查询上有权限

4）来宾/匿名访问模型被放宽

安全选项把网络访问搞得宽松。导致匿名也能进行枚举

## 为什么空不可以用anonymous可用用？

### impacket-lookupsid能成功，本质上就是连续“过了两道关”

### 1）SMB会话是否允许进入

（1）只决定：能不能建立会话/能不能访问共享/管道入口

（2）很多环境为了兼容，打印、游览等，仍允许匿名连接。

### 2）RPC接口是否授权（LSA/SAMR）

（1）决定：能不能调用LSA/SAMR的具体函数

（2）现代安全基线基本会把

​	（A）枚举用户/组

​	（B）SID<->名称解析

​	（C）SAM查询

​		收紧到“Authenticated Users”或者更高

### 所以场现实中会遇到

（1）SMB允许匿名连接

（2）但是RPC调用被拒绝（ACCESS_DENIED）