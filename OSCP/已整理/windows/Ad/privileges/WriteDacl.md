# WriteDacl

## 介绍

WriteDacl = 我不能动你，但是我能拿改“谁能动你”

WriteDacl是什么？

（1）允许你修改对象的DACL（访问控制列表）

（2）DACL决定：谁对这个对象拥有什么权限

（3）本身不等于控制对象，但可以变成完全控制

## WriteDacl的价值

### 1）WriteDacl=给自己（或别人）加任意权限

常见操作：

​	（1）给自己加GenriAll

​	（2）或加GenricWrite/WriteProperty（SPN）

一旦加完：你就等于拿下这个对象 

## 对[用户对象]WriteDacl能干什么？

1）改ACL->给自己GenericWrite/GenericAll

2）然后：

​	（1）改密码

​	（2）写SPN（Kerberoast）

​	（3）Shadow（Credential）

​	（4）完整接管用户

结论：WriteDacl=完全接管用户

## 对[计算机对象]WriteDacl能干什么？

（1）改Acl->给自己GenericWrite

（2）写msDS->AllowedToActOnBehalfOfOtherIdentity

（3）RBCD->System

结论：WriteDacl=计算机横向提权

## 对[组对象]WriteDacl能干什么？

1）你可以

​	（1）给自己加WriteMembers

​	（2）把自己加组

2）如果目标组是：

​	（1）Domain Admins

​	（2）Enterprise Admins

WriteDacl+组=秒DA

## 对[GPO/OU/Domain]

（1）GPO：改ACL->拿下恶意策略

（2）OU：控制整个OU

（3）Domain：DCSync/完全域控

## WriteDacl Vs GenericAll

| 权限       | 能直接做坏事 | 改ACL | 风险 |
| ---------- | ------------ | ----- | ---- |
| WriteDacl  | 不能         | 能    | 高   |
| GenericAll | 能           | 能    | 高   |

