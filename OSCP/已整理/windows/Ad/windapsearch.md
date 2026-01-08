# windapsearch

## 介绍

windaspsearch是一款专门用来通过LDAP枚举Active Directory的工具,在无凭据/低权限/有凭据三种情况下都非常好用..

本质=LDAP查询器+常用AD域模板枚举

## 攻击链的位置

典型 AD 攻击链里，windapsearch 在这里用：

```
端口发现 (389/636)
   ↓
windapsearch 枚举域信息   ← 你现在就在这一步
   ↓
确认用户 / 组 / 计算机
   ↓
Kerberos / SMB / Cert / ACL 攻击
```

## 它能枚举什么?

### 1)域基本信息

(1)域名(DN/FQDN)

(2)域功能级别

(3)域控信息(DC)

```
windapsearch -U --dc-ip 10.10.10.10 -d example.local
```

### 2)用户

(1)所有域用户

(2)管理员账号

(3)服务账号

(4)禁用/不可kerberos域认证用户(AS-REP Roasting)

```
windapsearch -U
windapsearch --da     # Domain Admin
```



### 3)组&域关系

(1)Domain Admins

(2)Remote Desktop Users

(3)Account Operators

(4)自定义高权限组

```
windapsearch -G
```

### 4)计算机

(1)所以域内主机

(2)DC/成员服务器/工作站

(3)主机+OS

```
windapsearch -C
```



#### 5)SPN(Kerberoasting)

(1)哪些账号绑定了SPN

(2)服务账号是谁

```
windapsearch --spns
```

## 匿名与认证枚举

### 1)匿名

```
windapsearch --dc 10.129.2.212 --full -m users
```

### 2)有凭据

```
windapsearch --dc 10.129.2.212 -u '' -p '' --full -m users
```

