# Kerberos-基础概念

## 域名在AD里是什么？

### 介绍

在AD中域名是一个安全边界，corp.local、ad.lab、offsec.internal

### 含义

这个名字下面

1）有一套用户

2）有一套组

3）一套计算机

4）一套kerberos体系

### 意义

1）我现在属于那个域

2）我能不能向这个域DC请求Kerberos票据

3）我拿到的凭据能不能在这个域横向使用

1）Kerberoast

2）AS-REP

3）横向

4）DA（Domain Admin)域管理员

## 什么是域结构？（Domain Structure）

域 (Domain)
	├── 域控 (Domain Controller)
	├── 域内机器 (Servers / Workstations)
	└── 域对象 (Users / Groups / Computers)

## 域控（Domain Controller,DC）

### 1.DC是什么

​	DC=域的大脑+认证中心+Kerberos KDC

它负责：

1）用户登录认证

2）发TGT/TGS

3）保存AD数据库

### 2.关注点

1）它叫什么？

2）在哪

## 域内机器（Members）

### 1.域内机器是什么

1）工作站（WS01）

2）服务器（APP01/SQL01/FILE01）

它们

1）加入了域

2）使用域账号登录

3）本地权限受域组影响

### 2.攻击视角（非常重要）

不是打所有视角

关心身份在哪台机器生效

## 域对象（Users/Groups)

### 1）域用户(Users)

1）普通用户

2）服务账号（SPN绑定）（svc_\*、service\*、sql\*、backup\*、app\*、web\*）

3）运维账号

### 2）域组(Groups)

1）Domain Admins （目标）

2）自定义管理组（一般有线索）

3）哪些账号“看起来不像普通用户”（不像人名的账号）admin、itadmin、operator、support

组=权限放大器

## 一般攻击路径

1）WS01（普通域账号）

2）Kerberoast

3）svc_sql

4）SQL01（本地管理员）

5）SYSTEM

6）域管理员凭据

7）DC01

## 目标选择优先级

### 1）普通域账号

corp\\user1

这个身份

1）大多数服务器!=管理员

2）在DC!=管理员

生效位置通常

1）它自己的服务站 2）被错误授权的机器

### 2）服务账号（Kerberoast后）

crop\\svc_sql 要立即想它是SQL账号一定在SQL服务上生效

正确选择：

1）SQL01（服务运行的机器）

服务账号通常只在跑它的服务机器上有权限

### 3）运维/备份账号

corp\\backup

这种账号特征

1）需要接触很多服务器

2）常被加入本地administrators

它的生效位置通常是：

FILE01、BACKUP01、管理服务器

### 4）总结

必须要思考我这个身份，在这台机器上会不会升维？

## 10秒判断

1）它是什么类型？

普通用户、服务账号、运维账号

2）它“为什么存在”？

给人登录、给服务跑、给运维用？

3）它必须在那台机器上工作？

服务->服务所在机器

运维->管理/服务器

普通用户->工作站