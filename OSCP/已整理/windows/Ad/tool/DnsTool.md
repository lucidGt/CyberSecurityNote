# dnstool

## 介绍

dnstool是利用AD集成DNS的“动态更新”权限，往DNS里加/删/改记录的工作。

本质LDAP->Microsoft DNS攻击面

## 参数

### 验证参数

| 参数       | 含义         | 说明                             |
| ---------- | ------------ | -------------------------------- |
| -u         | 域用户名     | 格式:domain\\\\user或domain/user |
| -p         | 密码         | 明文密码                         |
| -hashes    | LN:NT 哈希   | Pass-the-Hash                    |
| -k         | 使用kerberos | 使用票据认证                     |
| -no-pass   | 不提供密码   | 必须配合-k使用                   |
| KRB5CCNAME | Kerberos票据 | 通过环境变量指定.ccache          |

### DNS/DC参数

| 参数       | 含义          | 说明           |
| ---------- | ------------- | -------------- |
| 最后一个IP | DNS Server/DC | 位置参数       |
| -dc-ip     | 指定DC IP     | 有些版本需要填 |
| -dns-ip    | 指定DNS IP    | 等价于DC IP    |

### 动作参数

| 参数 | 含义           | 常见值                         |
| ---- | -------------- | ------------------------------ |
| -a   | action（动作） | add/delete/remove/query/modify |

### DNS参数

| 参数 | 含义        | 示例                          |
| ---- | ----------- | ----------------------------- |
| -r   | Record Name | evil.intelligence.htb或者evil |
| -d   | Record Data | A记录 = IP                    |
| -t   | Record Type | A/AAAA/CNAME/TXT/SRV          |
| -ttl | TTL         | 可选                          |



## 作用

在Active Directory里：

（1）DNS != 普通DNS

（2）DNS记录存储在AD对象中

（3）只要你有权限，就能写DNS

dnstool允许你：

（1）添加DNS记录

（2）删除DNS记录

（3）修改DNS记录

## 场景

### （A）NTLM Relay/强制认证

你加一个 DNS 记录，比如：

fileserver.intelligence.htb  →  10.10.14.66（你）

然后诱导某个服务访问：

\\fileserver\share

http://fileserver/

结果：

- 域内主机 **信你这个 DNS**
- 自动向你发起 **NTLM 认证**
- 你就可以：
  - ntlmrelayx
  - 拿 Net-NTLMv2
  - Relay 到 LDAP / SMB / ADCS

👉 **这是“无接触式横向移动”的基础组件**

### （B）配合 PetitPotam / PrinterBug / Coerce

流程是：

1. dnstool 加记录（指向你）
2. 强制 DC / 服务器访问该域名
3. DC 把 **高权 NTLM / Kerberos** 送给你

**dnstool = Coerce 攻击的“地基”**

### （C）绕过硬编码主机名

很多服务写死了主机名，例如：

backup.intelligence.htb

你没法控制服务，但你能控制 DNS 👉 **流量照样过来**

## 利用工具

### （1）添加一条A记录

python3 dnstool.py -u intelligence.htb/john.doe  -p 'Password123!' -r evil.intelligence.htb  -d 10.10.14.66 -t A 10.129.95.154

### （2）Kerberos票据方式

export KRB5CCNAME=administrator.ccache

python3 dnstool.py -k -no-pass -r evil.intelligence.htb -d 10.10.14.66 -t A dc.intelligence.htb

## 利用的条件

### ✅ 你具备以下任意之一：

（1）普通域用户

（2）DNSAdmins

（3）对MicrosoftDNS容器有Write权限

### 👉 **BloodHound 常见边：**

（1）WriteDacl

（2）GenericWrite

（3）DNSAdmins