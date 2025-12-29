# LSASS

## 介绍

LSASS(Local Security Authority SubSystem Service),是Windows进行凭据认证系统。

它负责

1）登录认证

2）凭据管理

3）安全策略

4）会话安全上下文

它不是执行权限判断的地方，而是发证机关。

## LSASS里到底有什么？

### 1）登录凭据

明文密码（特定场景）

NTLM HASH

Kerberos TGT/TGS

DPAPI Master Key的材料

Credential Cache

### 2）Kerberos相关数据（域环境）

在域环境下,LSASS会缓存

1）Kerberos会话

2）TGT（Ticket Granting Ticket）

3）Service Ticket

4）域SID/用户SID映射

### 3）安全上下文信息

1）当前登录会话（Logon Session）

2）登录类型（Interactive/Service/Network）

3）LUID（Logon ID）

4）对应的用户身份信息

LSASS用这些信息请求内核生成Token

### 4）本地安全策略/授权数据

1）用户属于那些组

2）应有那些特权

3）本地/域安全策略结果

## LSASS绝对没有的东西

### 没有Access Token

Token在内核内存上

### 没有ACL

ACL在对象上（文件/注册表/服务）

### 没有SID->Token的绑定结果

只有可用于生成Token的信息

## LSASS提权过程

1）读LSASS（SeDebugPrivilege）

2）拿到凭据、票据

3）重新登录/建立会话

4）内核生成新Token

5）权限提升