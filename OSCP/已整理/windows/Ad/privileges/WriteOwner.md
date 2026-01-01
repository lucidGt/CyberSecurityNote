# WriteOwner

## 介绍

WriteOwner=我能把“对象的主人”改成我自己

## WriteOwner是什么？

1）允许你修改对象的Owner（所有者）

2）在AD中

​	Owner有权修改对象的DACL

3）所以逻辑是

​	（1）WriteOwner->我成Owner->我能改DACL->我给自己GnericAll->我完全控制对象

## 对[用户对象]WriteOwner是什么？

（1）把Owner改成自己

（2）改DACL->给自己GenericAll/GenericWrite

（3）改密码/SPN/Shadow Credentials

结论：WriteOwner->用户=完全接管

## 对[计算机对象]WriteOwner是什么？

（1）成Owner

（2）改DACL

（3）RBCD/Shadow Credentials/SYSTEM

WriteOwner->计算机=横向入口

## 对[组对象]WriteOwner是什么？

1）成Owner

2）给自己加WriteMembers

3）把自己加组

如果目标是：

​	（1）Domain Admins

​	（2）Enterprise Admins

结论：WriteOwner->组=秒DA

## 对[GPO/OU/Domain]WriteOwner是什么？

（1）GPO：完全接管策略

（2）OU：控制链OU

（3）Domain：DCSync/域控

## WriteOwner vs WriteDacl

| 权限       | 改DACL | 是否最终可控 |
| ---------- | ------ | ------------ |
| WriteDacl  | 可以   | 可以         |
| WriteOwner | 先不行 | 滥用         |

writeOwner不比WriteDacl弱只是多一步

