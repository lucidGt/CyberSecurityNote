# NTLM（NT LAN Manager）

## 介绍

NT->New Technology

LAN->Local Area Network

Mnager->管理认证

Windows NT时代的局域网认证管理协议。

## 能做（PTH）Pass The Hash的服务

凡是基于NTLM challenge-response的Windows远程管理/RPC服务都能PTH。

### SMB（445）

文件共享

远程服务管理

远程命令执行

psexec

smbexec

wmiexec

creackmapexec smb

### WMI（135+445）

Windows管理接口

本质走RPC/SMB

完全支持用Hash

### WinRM（5985/5986）

Windows Remote Management

PowerShell远程

很多环境下能直接PTH

### MSSQL（1433/Windows Auth）

使用NTLM集成

可以直接用HASH登录

后续xp_cmdshell->RCE

## 条件性PTH的服务

### HTTP/HTTPS（80/443）（IIS+NTLM）

Web启用Windows Integrated Authentication

NTLM/Negotiate

特定情况下PTH

## 不能PTH的服务

### RDP（3389）

可以用NTLM

不能直接HASH登录

需要明文或者Kerberos

### Kerberos（88）

完全另一套体系

用票据（TGT/TGS）

hash在这里没用

### LDAP（389/636）

查询命令

不能用于PTH登录

### DNS/SNMP/SMTP

不做NTLM认证

纯信息服务

