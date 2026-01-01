# servicePrincipalName

## 介绍

SPN (servicePrincipalName) = Kerberos“某个服务的唯一身份证号”

在AD/Kerberos中：

​	（1）用户!=服务

​	（2）Kerberos认证的对象是：服务

​	（3）SPN来告诉KDC：“某个服务是由那个账号运行的”

## SPN的本质

### SPN是一个属性

### 1）存在于：

​	（1）用户对象（服务账号）

​	（2）计算机对象（机器账号）

### 2）属性名：servicePricipalName

### 3)一对多的关系：

​	（1）一个账号->多个SPN

​	（2）一个SPN->只能属于一个账号

## SPN长什么样？

### 1）常见格式：

```
service/hostname
service/hostname:port
service/hostname@REALM
```

### 2）常见样例

```
HTTP/web.administrator.htb
MSSQLSvc/sql01.administrator.htb:1433
CIFS/DC01.administrator.htb
HOST/WEB01
```

## SPN是干嘛用的（正常流程）

1.客户端要访问某个服务（比如MSSQL）

2.客户端向KDC请求：“我要访问SPN=MSSQLSVC/sql01:1433”

3.KDC查AD：这个SPN绑定在那个账号上？

4.KDC用该账号的密钥（密码）加密TGS并返回

5.客户端拿TGS去访问

重点：TGS是用“服务账号的密码”加密的

## 为什么SPN能被用来攻击？

关键

（1）任何域用户都可以请求任何SPN的TGS

（2）不需要是管理员

（3）不需要知道服务账号密码

## 为什么给普通账号加SPN会出事？

1）KDC不关心：

​	（1）这个账号是不是“真的服务”

2）KDC只认

​	（1）SPN是否存在

​	（2）绑定在那个账号

所以：

```
普通用户
+ 你能写 servicePrincipalName
→ 变成“服务账号”
→ 可被 Kerberoast
```

这就是targeted Kerberoast

## SPN和这些攻击的关系

| 攻击              | SPN角色           |
| ----------------- | ----------------- |
| Kerberoast        | 核心目标          |
| Target Kerberoast | 人为制造目标      |
| Delegation        | SPN定义“谁是服务” |
| Silver ticket     | SPN决定票据的作用 |

## 提醒

1）SPN不能重复

2）写错/冲突SPN

​	（1）会破坏业务

​	（2）会被监控

3）所以实战中：

​	（1）选一个唯一、假的SPN

​	（2）用完就删