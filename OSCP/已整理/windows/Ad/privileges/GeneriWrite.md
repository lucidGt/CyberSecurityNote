# GeniricWrite

## 介绍

GenericWrite=能“随便写”对象的大部分属性，但不能改ACL/Owner

### 1）GeneriWrite是什么？

（1）允许写对象的大多数属性

（2）不包括：改DACL、改Owner（这是个GeniricAll的核心去呗

（3）但：很多关键攻击点本来就在“属性”上

## 对[用户对象]GenericWrite能干什么？

（1）写SPN->Kerberoast/targeted Kerberroast

（2）写msDS-KeyCrendentialLink->Shadow Credentials （证书登录）

（3）改UPN->证书/Kerberos滥用

（4）改description/scriptPath/profilePath->留后门/凭据投递

不能直接改ACL/Owner

结论：对用户拥有GenericWrite=迟早能接管整个用户

## 对[计算机对象]GenericWrite能干什么？

（1）写msDS-AllowedToActOnBehalfOfOtherIdentity->RBCD（资源约束委派）

（2）写SPN

（3）Shadow Credentials

不能改DACL/Owner

对计算机有GeneriWrite=System/横向入口

## GenericWrite和GenericAll的核心？

| 权限         | 能写属性 | 能改ACL | 能改Owner |
| ------------ | -------- | ------- | --------- |
| GenericWrite | ×        | ×       | ×         |
| GenericAll   | ✔        | ✔       | ✔         |

## 优先级

（1）对象类型

（2）SPN->Kerberoast

（3）KeyCrendential->Shadow Crendentials

（4）RBCD（如果是计算机）

