# ldapdomaindump

## 介绍

ldapdomaindump是一个用来把Active Directory的结构信息从LDAP拉下来枚举的工具

## 原理

LDAP查询，Active Directory本质就是一个LDAP目录。

域里的：

​	（1）用户（2）组（3）计算机（4）OU（5)GPO都可以通过LDAP搜索查询

普通域用户就有大量LDAP读取权限

## ldapdomaindump vs BloodHound

| 工具           | 定位                      |
| -------------- | ------------------------- |
| ldapdomaindump | 快速、直观、轻量的AD枚举  |
| BloodHound     | 深度关系分析/攻击路径计算 |

ladpdomaindump：“导出地图”

BloodHound：“算最优进攻路线”

1.先ldapdomaindump看整体

2.再决定跑不跑bloodHound

## 命令

ldapdomaindump -u management.htb\\operator -p 'operator' 10.10.11.236 -o ldap/
