# DCSync

## 介绍

DCSync = 假装自己是域控，向真正的域控“同步账号数据”

1）在正常的AD中：

​	（1）域控之间需要同步用户、密码、Hash

​	（2）这个同步过程叫Directory Replication

2）DCSync攻击就是：

​	利用AD复制协议，远程把整个域账号的hash复制过来。

不需要在DC上执行命令

不需要本地管理员

纯协议级攻击

## DCSync能拿到什么？

成功后，你能拿到：

​	（1）所有域用户的NTLM hash

​	（2）krbtgt hash

​	（3）域管理员 hash

​	（4）计算机账号 hash

一旦拿到krbtgt

​	（1）Golden Ticket

​	（2）永久域后门

基本等价于“域沦陷”

## 为什么它这么危险

1）因为：

​	（1）它不是漏洞

​	（2）是合法的功能滥用

​	（3）很多环境默认没监控

2）而且：

​	（1）不需要代码主席

​	（2）不需要登录DC

​	（3）可以从任意一台机器发起

## DCSync需要什么权限

 你对Domain对象必须具有以下权限之一：

1）必须具备ExtendedRights：

​	（1）Replicating Directory Changes

​	（2）Replicating Directory Changes All

​	（3）（有时候还包括）Replicating Directory Changes in Filtered Set

2）哪些“高阶权限”天然包含它？

​	（1）Domain Admins

​	（2）EnterPrise Admins

​	（3）Administrators（域）

​	（4）AllExtendedRights（在Domain对象上）

​	（5）GenericAll（在Domain对象上）

3）重点AllExtendedRights+Domain = DCSync

## BloodHound怎么看DCSync

1）如果你看到

```
User → Domain
AllExtendedRights
```

2）或者

```
User → Domain
GetChanges / GetChangesAll
```

直接DCSync路线

## 实战中DCSync怎么用？

常见工具

1）mimikatz(lsadump::dcsync)

2）secretsdump.py(impacket)

流程（概念）

```
有复制权限
→ 向 DC 发 replication 请求
→ DC 返回账号 hash
→ 离线利用 / 票据攻击
```

## DCSync和Kerberoast的区别

| 项目 | Kerberoast     | DCSync     |
| ---- | -------------- | ---------- |
| 目标 | 单个服务账号   | 整个域     |
| 权限 | 普通域用户即可 | 复制权限   |
| 结果 | hash(少量)     | hash(全部) |
| 级别 | 横向/提权      | 域控沦陷   |

## 提醒

1）DCSync日志明显

2）很多企业会监控