# English

## 核心词汇

| 英语                          | 理解               |
| ----------------------------- | ------------------ |
| enumerate                     | 枚举/找信息        |
| exploit                       | 利用漏洞           |
| execute                       | 执行（命令+代码）  |
| escalate                      | 提权               |
| authenticate                  | 认证               |
| bypass                        | 绕过               |
| abuse                         | 滥用（配置/权限）  |
| obtain                        | 获取               |
| retrieve                      | 拿到               |
| spawn                         | 弹出（Shell/进程） |
| inject                        | 注入               |
| dump                          | 导出（凭据/内存）  |
| Remote  Code Execution（RCE） | 远程执行           |
| Arbitrary Code Execution      | 任意代码执行       |
| Command Inject                | 命令注入           |
| Unauthenticated               | 无需认证           |
| File Upload                   | 文件上传           |
| Deserialization               | 反序列化           |
| SQL Injection                 | SQL注入            |
| Privilege Escalation          | 本地提权           |
| SUID                          | SUID提权           |
| Writable                      | 可写               |
| Readable                      | 可读               |
| DLL Hijacking                 | DLL劫持            |
| Crash                         | 崩溃               |
| Memory Leak                   | 内存泄露           |
| Poc Only                      | 没完整利用         |
| Requires user interaction     | 玄学               |
| Authenticated                 | 需要账号           |
| Require valid credential      | 需要密码           |
| Post-auth                     | 登录后             |
| misconfigured service         | 配置错误           |
| hardcode credentials          | 硬编码密码         |

## 权限/身份

| 英语          | 理解            |
| ------------- | --------------- |
| privilege     | 权限            |
| administrator | 管理员          |
| standard user | 普通用户        |
| SYSTEM        | Windows最高权限 |
| root          | Linux最高权限   |
| credential    | 凭据            |
| password      | 明文密码        |
| hash          | 哈希            |
| token         | 令牌            |
| impresonate   | 冒充            |

## 网络/服务

| 英语             | 含义      |
| ---------------- | --------- |
| service          | 服务      |
| listening on     | 监听      |
| port             | 端口      |
| share            | 共享      |
| endpoint         | 接口      |
| connection       | 连接      |
| request/response | 请求/响应 |

##  Exploit描述

| 英语                           |      |
| ------------------------------ | ---- |
| remote   code execution（RCE） |      |
| arbitrary code execution       |      |
| privilege escalation           |      |
| unauthenticated                |      |
| authenticated                  |      |
| local user                     |      |
| denial of service              |      |

## 报告结构

1.Information Gathering

2.Service Enumeration

3.Inital Access

4.Privilege Escalation

5.Post-Exploitation

## 模块1.Information Gathering（信息收集）

We performed an initial network scan to identify live hosts and open ports.

Nmap was used to enumerate services running on the target machine.

## 模块2.Service Enumeration（服务枚举）

An SMB  service was identified on port 445.

Anonymous access was enabled on the SMB share

This allowed us to list and download files from the share.

## 模块3.Initial Access（初始突破）

A vulnerability was identified in the web application.

This vulnerability allowed remote code execution.

A reverse shell was obtained by exploiting this issue.

## 模块4.Privilege Escalation（提权）

Linux例子

The current user was a low-privileged user.

A writable SUID binary was identified.

By abusing this binary,root privileges were obtained.

Windows例子

The user had SeImpersonatePrivilege enabled.

This allowed privilege escalation to SYSTEM using PrintSpoofer.

## 模块5：Proof

The following screenshot show;

- Output of proof.txt
- Output of whoami
- Network configuration.