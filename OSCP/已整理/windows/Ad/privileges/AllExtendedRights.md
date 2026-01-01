# AllExtendedRights

## 介绍

AllExtendedRights = 允许你执行对象上“所有定义的扩展权限（Extended Rights）”

## 什么是AllExtendedRights?

在AD中，权限分三大类：

1）标准权限（Standard Rights）

​	（1）Read/Write/ChangeOwner等

2）属性权限（Property Rights）

​	（1）WriteProperty:servicePrincipalName

​	（2）WriteProperty:msDS-KeyCredentialLink

3）扩展权限（Extended Rights）

​	（1）Reset Password

​	（2）Force Change Password

​	（3）DCSync（在Domain对象上）

​	（4）某些Kerberos/证书相关操作上

重点：Extended Rights不等于写权限

## 对[用户对象]AllExtendedRights是什么？

（1）Reset Password

（2）Force Change Password at next Logon

（3）有时能触发某些Kerberos行为（不稳定）

结论：AllExtendedRights->用户=控制力有限

## 对[计算机对象]AllExtendedRights是什么？

（1）Reset机器账户密码

（2）某些委派相关扩展权限

## 对[Domain对象]AllExtendedRights是什么？

1）DCSync

​	（1）Replicating Directory Changes

​	（2）Replicating Directory Changes All

2）一键dump域所有账号hash

结论：AllExtentedRights->Domain=直接域沦陷

## 为什么AllExtendedRights没有想的那么强？

（1）它不包含属性写权限

（2）不能写SPN

（3）不能Shadow Credentials

（4）不能RBCD

（5）不能改ACL

所以在用户/计算机对象上：

​	它远不如GenericWrite/WriteProperty

## BloodHound怎么看AllExtendedRights影响力

1）看对象是谁

2）如果是：

​	（1）Domain对象->高危（DCSync）

​	（2）用户/计算机->中等