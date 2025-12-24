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
| save credentials（savecred）  | 使用缓存的凭据     |
| run as                        | 以某个用户身份运行 |
| reconnaissance（recon）       | 侦擦               |
| identify                      | 识别               |
| fingerprint                   | 指纹识别           |
| discover                      | 发现               |
| scan                          | 扫描               |
| probe                         | 探测               |
| trigger                       | 触发               |
| gain code execution           | 获得代码执行       |
| obtain a shell                | 拿到shell          |
| foothold                      | 立足点             |
| Interal movement              | 横向一栋栋         |
| reuse credentials             | 复用凭据           |
| pivot                         | 跳板/转发内网      |
| domain compromise             | 拿下域             |

## 万能句型

1）我做了什么（方法）

During infomation gathering, identified the target hosts in sacope.

During service enumeration,I enumerated open port and ruining service.

2）我发现了什么（证据）

 Port 445/tcp was open, indicating SMB was exposed.

The web server revelaed a login page running X.

3）我怎么拿下的（动作）

I exploited vulnerability to obtain an install shell.

I the performed privilege escalation to gain administrative access.

4）我怎么证明（验证）

Proof was obtained by reading proof.txt and verifying the current user with whoami/d

## 常用

runas：以另一个身份运行（Run as another user）

/savecred：保存凭据（save credentials / cached credentials）

cached credentials：缓存凭据

stored credentials：已保存凭据

## 术语

1.枚举类动词（enumerate/identify/discover/fingerprint）

2.漏洞利用类（explit/trigger/RCE/foothold）

3.提权类（misconfiguration/privilege escalation/abuse）

4.AD/横向类（later movement/ahthenticate/pivot）

## 	权限/身份

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