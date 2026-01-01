# GenericAll

## 介绍

GenericAll=对该对象“完全控制”，在AD里，它基本等价于“你是这个对象的主人”

（1）AD对象的一个通用访问控制权限

（2）覆盖：读/写所有属性+改ACL+改Owner+执行扩展操作

（3）作用对象：用户/计算机/组/GPO/OU/域对象

## 对[用户对象]有GenericAll能干什么？

### 1）利用

（1）改密码

（2）写SPN->Kerborast/targeted Kerberoast

（3）写msDS-KeyCredentialLink->shadow Credentials （证书/Key攻击）

（4）改UPN/SIDHistory/description/mail等

（5）加自己到该用户的可控攻击链

### 2）间接后果

（1）如果把该用户升级成攻击跳板

（2）如果目标是高权限用户（Domain Admin）=域沦陷

## 对[计算机用户]有GenericAll能干什么？

### 1）利用

（1）重置机器账户密码

（2）写SPN

（3）写msDS-AlowedToActOnBehalfOfOtherIdentity->RBCD（资源约束委派）

（4）shadow Credentials（如果环境支持）

（5）最终：横向/提权到System

## 对[组对象]有GenericAll能干什么？

### 1）利用

往组里加人

​	如果是：

​	（1）Domain Admins

​	（2）Enterprise Admins

​	（3）Administrators

​		直接域控

## 对[GPO/OU/域对象]有GenericAll能干什么？

（1）GPO：下放恶意策略（本地管理员、启动脚本）

（2）OU：控制整个OU下所有对象

（3）Domain对象：

​	1）DCSync

​	2）域级完全控制

​	3）Game over