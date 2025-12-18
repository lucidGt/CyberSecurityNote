# Windows命令命名规则

## 原则

Windows命令名 = 英语缩写 + 工程师命名

## 服务/计划任务

| 命令     | 英语                | 理解                    |
| -------- | ------------------- | ----------------------- |
| sc       | Service Control     | 管服务的（查/启/停/配） |
| sc qc    | Query Configuration | 查服务怎么配置的        |
| sc query | Query Status        | 查服务状态              |
| schtasks | scheduled Tasks     | 管计划任务的            |
| /query   |                     | 查询                    |
| /fo LIST | format ouput = LIST | 以列表形式输出          |
| /v       | verbose             | 详细信息给我            |

## 权限/用户

| 命令          | 英语       | 理解         |
| ------------- | ---------- | ------------ |
| whoami        | who am i   | 我现在是谁   |
| whoami /priv  | privileges | 我有什么权限 |
| whoami/groups | groups     | 我在哪些组   |

## 权限/文件

| 命令     | 英语                             | 理解             |
| -------- | -------------------------------- | ---------------- |
| icacls   | (I) Change ACLs                  | 谁能访问这个文件 |
| ACL      | Access Control List              | 权限清单         |
| F/M/W/RX | Full/Modify/Write/Read-Execution | 权限级别         |

## 注册表

| 命令      | 英语               | 人话         |
| --------- | ------------------ | ------------ |
| reg       | Registry           | 管注册表     |
| reg query | query              | 查键值       |
| HKLM      | HKEY_LOCAL_MACHINE | 全局配置     |
| HKCU      | HKEY_CURRENT_USER  | 当前用户配置 |

## 系统/网络

| 命令           | 英语           | 人话     |
| -------------- | -------------- | -------- |
| net user       | network user   | 用户     |
| net localgroup | local group    | 本地组   |
| Administrators | administrators | 管理员组 |

## Windows/AD核心服务

| 缩写  | 英语                                       | 人话                      |
| ----- | ------------------------------------------ | ------------------------- |
| SMB   | Server Message Block                       | Windows文件/共享/认证协议 |
| RPC   | Remote Procedure Call                      | 远程调用Windows功能       |
| LSA   | Local Security Authority                   | 本地安全认证核心          |
| LSASS | Local Security Authority SubSystem Service | 管密码/票据的进程         |
| SAM   | Security Account Manager                   | 本地账号数据库            |
| DC    | Domain Controller                          | 域控（AD大脑）            |
| AD    | Active Directory                           | 域身份管理系统            |
| GPO   | Group Policy Object                        | 域策略                    |
| OU    | Organizational Unit                        | AD里的部门/容器           |

SMB/LDAP/Kerberos -> AD

LSASS/NTLM/TGT/TGS->凭据/票据

MSI/AIE->提权

WinRM/RDP/SMB->横向

DNS/AXFR->资产暴露

## 认证/身份

| 缩写     | 英语                             | 人话                |
| -------- | -------------------------------- | ------------------- |
| NTLM     | NT LAN Manager                   | 老的Windows认证方式 |
| Kerberos | Kerberos Authentication Protocol | 域里用的主认证协议  |
| TGT      | Ticket Granting Ticket           | Kerberos的总票据    |
| TGS      | Ticket Granting Service          | 访问具体服务的票据  |
| SPN      | Service Principal Name           | 服务在域里的身份证  |
| UAC      | User Account Control             | 管理员权限确认机制  |
| AIE      | AlwaysInstallElevated            | MSI提权配置         |

## 网络/端口

| 缩写  | 英语                                  | 端口      | 理解           |
| ----- | ------------------------------------- | --------- | -------------- |
| FTP   | File Transfer Protocol                | 21        | 文件传输       |
| SSH   | Secure Shell                          | 22        | 远程终端       |
| SMTP  | Simple Mail Transfer Protocol         | 25        | 发邮件         |
| DNS   | Domain Name System                    | 53        | 域名解析       |
| HTTP  | HyperText Transfer Protocol           | 80        | Web            |
| HTTPS | HTTP Secure                           | 443       | 加密web        |
| LDAP  | Lightweight Directory Access Protocol | 389       | 查AD           |
| LDAPS | LDAP Secure                           | 636       | 加密LDAP       |
| RDP   | Remote Desktop Protocol               | 3389      | 远程桌面       |
| WinRM | Windows Remote Management             | 5585/5586 | 远程PowerShell |

## Windows服务/进程

| 缩写 | 英语                                | 人话            |
| ---- | ----------------------------------- | --------------- |
| SCM  | Service Control Manager             | 管理所有服务    |
| SVC  | Service                             | 服务            |
| EXE  | Executable                          | 可执行文件      |
| DLL  | Dynamic Link Library                | 动态链接库      |
| MSI  | Microsoft Installer                 | 安装包          |
| PS   | PowerShell                          | Windows脚本环境 |
| CMD  | Command                             | 命令行          |
| WMI  | Windows  Management Instrumentation | 远程管理接口    |

## Linux/Web/常见

| 缩写  | 英语                               | 人话         |
| ----- | ---------------------------------- | ------------ |
| NFS   | Network File System                | 网络文件共享 |
| SNMP  | Simple Network Management Protocol | 设备管理     |
| SQL   | Structured Query Language          | 数据库       |
| API   | Application Programming Interface  | 程序接口     |
| CMS   | Content Management System          | 内容管理系统 |
| CI/CD | Continuous Integration/Deployment  | 自动构建部署 |



## 经常遇到缩写

| 缩写        | 英语                | 理解         |
| ----------- | ------------------- | ------------ |
| qc          | Query Configuration | 配置         |
| query       | query               | 状态/内容    |
| priv        | privilege           | 特权         |
| svc         | service             | 服务         |
| exe         | executable          | 可执行程序   |
| ps1         | PowerShell script   | 脚本         |
| cmd         | command             | 命令         |
| Run As User | run as              | 用谁的权限跑 |