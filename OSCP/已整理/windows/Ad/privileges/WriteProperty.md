# WriteProperty

## 介绍

WriteProperty = 允许你“写某些指定属性”（不是全部）

在AD中：

​	（1）每个对象（User/Computer/Group/GPO）都有很多属性

​	（2）ACL可以精确到某一属性

​	（3）writeProperty就是你必允许“某些属性”

## WriteProperty:servicePrincipalName

### 1）能干什么？

（1）给普通用户加SPN

（2）改已有SPN（小心冲突）

（3）配合GetUserSPNs请求TGS

### 2）在BloodHound怎么显示？

​	（1）WriteSPN、WriteProperty

## WriteProperty:msDS-KeyCreDentialLink

### 1）能干什么？

（1）能写Key Credential

（2）->Shadow Credentials

（3）->直接证书登录用户

比Kerberoast更稳

## WriteProperty:userAccountControl

### 1）能干什么？

（1）可启用/禁用账号

（2）可配合其他攻击链

（3）单独价值一般

## WriteProperty:scriptPath/profilePath/homeDirectory

### 1）能干什么？

（1）可以用于登录脚本劫持

（2）依赖用户交互