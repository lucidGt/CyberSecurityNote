# CrackMapExec

## 介绍

CrackMapExec（CME）是一个域内攻击/枚举框架。

我有一组凭据，现在想在域内快速判断：我能干什么，我能打哪里，哪里有坑

 多协议并行枚举+凭据有效性验证+横向条件判断+模块化漏洞检查

| 协议  | 用途      | 典型场景       |
| ----- | --------- | -------------- |
| SMB   | 主要      | 横向、权限判断 |
| LDAP  | 域情报    | AD/AD CS       |
| WinRM | 远程命令  | 高权限横向     |
| RDP   | 登录验证  | 桌面访问       |
| MSSQL | SQL横向   | 服务账号滥用   |
| SSH   | Linux主机 | 混合环境       |

## 参数

### 协议参数

| 参数  |                  |
| ----- | ---------------- |
| smb   | SMB枚举/权限判断 |
| ldap  | AD/域枚举        |
| winrm | WinRM登录测试    |
| mssql | MSSQL 登录/枚举  |
| rdp   | RDP登录测试      |
| ssh   | SSH登录测试      |

### 身份参数

#### （1）用户密码

| 参数      | 含义   |
| --------- | ------ |
| -u USER   | 用户名 |
| -p PASS   | 密码   |
| -d DOMAIN | 域名   |

#### （2）Hash（Pass-The-Hash）

| 参数         | 含义      |
| ------------ | --------- |
| -H HASH      | NTLM Hash |
| --local-auth | 本地账号  |

### 枚举类参数

| 参数             | 作用         |
| ---------------- | ------------ |
| --shares         | 枚举SMB共享  |
| --sessions       | 当前登录会话 |
| --loggedon-users | 已登录用户   |
| --users          | 域用户       |
| --groups         | 域组         |
| --computers      | 域计算机     |
| --local-groups   | 本地组       |
| --pass-pol       | 密码策略     |

### 模块参数 -M

-M <module>

| 模块           | 作用        |
| -------------- | ----------- |
| adcs           | 枚举ADCS    |
| laps           | 枚举LAPS    |
| gpp_autologin  | GPP明文密码 |
| enum_users     | 枚举用户    |
| enum_groups    | 枚举组      |
| enum_computers | 枚举计算机  |

### 慎用模块

| 模块        | 风险           |
| ----------- | -------------- |
| mimikatz    | 内存抓凭据     |
| lsassy      | 自动dump LSASS |
| hash_spider | 自动横向抓Hash |

### 输出/扫描辅助参数

| 参数                  | 作用         |
| --------------------- | ------------ |
| --continue-on-success | 成功后继续扫 |
| --timeout             | 超时         |
| --threads             | 线程数       |
| --verbose             | 详细输出     |



## 凭据验证

 支持凭据类型：

（1）明文密码

（2）NTLM Hash（Pass-The-Hash）

（3）Kerberos部分场景

## 权限判断

| 标志                    | 含义                 |
| ----------------------- | -------------------- |
| Pwn3d!                  | 当前用户是本机管理员 |
| ADMIN                   | 本地管理员           |
| Domain Admin            | 域管理员             |
| SMB signing：True/False | 是否能relay          |
| OS/Domain/Hostname      | 目标环境             |

## 横向移动辅助

### 1）远程执行（条件满足时）

(1)cmd

crackmapexec smb target -u user -p pass -x "whoami"

(2)PowerShell

crackmapexec smb target -u user -p pass -X "Get-Process"

### 2）WinRM横向

crackmapexec wimrm target -u user -p pass

适合：

（1）服务账号

（2）域内管理员账号

## LDAP枚举

| 能力       | 说明            |
| ---------- | --------------- |
| 枚举域信息 | 域名、DC        |
| 枚举用户   | 用户列表        |
| 枚举组     | Domain Admins等 |
| 枚举机器   | 计算机对象      |
| 枚举ACL    | 权限关系        |
| 枚举AD CS  | 证书服务        |

## 模块系统

### AD/域相关

| 模块          | 干什么         |
| ------------- | -------------- |
| adcs          | 检查ad证书提权 |
| gpp_autologin | 查GPP明文密码  |
| laps          | 查LAPS密码     |
| enum_users    | 用户枚举       |
| enum_groups   | 组枚举         |

### 凭据相关

| 模块             | 干什么       |
| ---------------- | ------------ |
| lsassy           | 远程抓LSASS  |
| mimikatz         | 调mimikatz   |
| hash_spider      | 横向搜hash   |
| credential_guard | 检查是否开启 |

### 服务类

| 模块        | 干什么       |
| ----------- | ------------ |
| mssql       | SQL枚举      |
| spider_plus | 共享文件爬取 |
| webdav      | WebDAV检查   |

## 环境判断

（1）这个网段有没有DC?

（2）SMB signing开了吗？

（3）NTLM是否可用？

（4）Kerberos是否强制？

（5）我现在这组凭据是不是废的？

