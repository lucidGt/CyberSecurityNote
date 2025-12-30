# adsearch

## 介绍

adsearch是一个轻量级LDAP枚举工具，本质就是“命令行版LDAP查询器”

对域控的LDAP发查询，返回AD对象属性

枚举 **域用户 / 组 / 计算机**

查 **SPN（Kerberoasting）**

查 **AS-REP 可爆破用户**

查 **委派、ACL、GMSA**

验证 BloodHound 发现的东西

## 语法参数

adsearch [认证参数] [连接参数] [搜索参数]

### 认证参数

| 参数      | 含义                 |
| --------- | -------------------- |
| -u USER   | 域用户名             |
| -p PASS   | 密码                 |
| -d DOMAIN | 域名                 |
| -k        | Kerberos认证（用票） |
| -H HASH   | NTLM Hash            |

匿名LDAP

adsearch -d example.com -s base

### 连接参数

| 参数      | 含义       |
| --------- | ---------- |
| -h DC_IP  | 域控IP     |
| -p 389    | LDAP端口   |
| -p 636    | LDAPS端口  |
| -e        | 使用SSL    |
| -b BASEDN | 搜索基准DN |

BASEDN示例：DC=example,DC=com

### 搜索参数

| 参数       | 含义         |
| ---------- | ------------ |
| -s subtree | 子树搜索     |
| -s base    | 只查base DN  |
| -f FILTER  | LDAP 过滤器  |
| -a ATTR    | 指定返回属性 |
| -A         | 返回所有属性 |
| -l LIMIT   | 返回条数限制 |

## 利用

### （1）枚举所有域用户

adsearch -h 10.10.10.10 -d example.com -u user -p pass -b "DC=example,DC=com" -s subtree -f "(objectClass=user)"

### （2）枚举域计算机

-f "(objectclass=computer)"

### （3）Kerberoasting（有SPN用户）

-f "(&(objectClass=user)(servicePrincipalName=*))" -a sAMAccountName servicePrincipalName

找到就能GetUserSPNs.py

### （4）AS-REP Roasting（不用预认证的用户）

-f "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" -a sAMAccountName

这一步等价BloodHound 的 PreauthNotRequired

### （5）枚举组+成员

-f "(objectClass=Group)" -a cn member

### （6）找委派相关

#### （A)非约束委派

-f "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))"

#### （B）约束委派

-f "(msDS-AllowedToDelegateTo=*)"

#### （C）资源约束委派

-f "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)"

同时看谁被委派

-a dn msDS-AllowedToActOnBehalfOfOtherIdentity

### （7）查 GMSA

-f "(objectClass=msDS-GroupManagedServiceAccount)" -a sAMAccountName msDS-ManagedPassword

## 与其他工具对应位置

| 目的   | adsearch           | BloodHound / PowerView  |
| ------ | ------------------ | ----------------------- |
| 查 SPN | LDAP filter        | GetUserSPNs             |
| AS-REP | LDAP filter        | PreauthNotRequired      |
| 委派   | userAccountControl | UnconstrainedDelegation |
| 用户   | objectClass=user   | Get-DomainUser          |
| 组     | objectClass=group  | Get-DomainGroup         |

