# 🪟 Windows 提权

> 目标：从普通用户 → Administrator/SYSTEM
> 原则：先“配置错误/权限错误”，最后才考虑漏洞利用。

---

## 0) 先稳住：确认身份 & 环境（1分钟）

- [ ] whoami
- [ ] whoami /groups
- [ ] whoami /priv
- [ ] hostname
- [ ] systeminfo
- [ ] echo %USERNAME% & echo %USERDOMAIN%
- [ ] ipconfig /all
- [ ] net users
- [ ] net localgroup administrators
- [ ] net localgroup "Remote Management Users"
- [ ] query user

**重点看：**

- 是否在 Administrators 组
- 是否有高价值特权：SeImpersonatePrivilege / SeAssignPrimaryToken / SeBackup / SeRestore / SeDebug 等
- 是否是域环境（%USERDOMAIN% / systeminfo 域信息）

---

## 1) 立刻查“可直升”的配置（高命中）

### 1.1 UAC / Token / 管控

- [ ] reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
- [ ] reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
- [ ] reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy
- [ ] reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v PromptOnSecureDesktop

### 1.2 AlwaysInstallElevated（少见但送分）

- [ ] reg query HKCU\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
- [ ] reg query HKLM\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

（两边都为 1 才是命中点）

---

## 2) 服务相关提权（OSCP 高频：必查）

### 2.1 列出服务（先找“第三方/自写”）
- [ ] sc query state= all
- [ ] wmic service get Name,DisplayName,PathName,StartMode

**重点找：**

- PathName 指向非系统目录（如 C:\Program Files\Vendor\...）
- 可疑 EXE/DLL 路径、带空格路径

### 2.2 Unquoted Service Path（未加引号路径）

命中条件：
- 服务路径有空格
- 没有被双引号包裹
- 你对某个可被“插入”的路径位置有写权限

辅助检查：
- [ ] sc qc <ServiceName>

### 2.3 服务二进制/目录权限错误

- [ ] icacls "C:\Path\to\service.exe"
- [ ] icacls "C:\Path\to\service\folder\"

你要找的权限：
- Users / Authenticated Users / 某普通用户 对 EXE 或目录有 (M)/(F)

### 2.4 服务可修改（更直接）

- [ ] sc sdshow <ServiceName>

（看是否能改 binPath / config；常用工具会更好读）

---

## 3) 计划任务（Scheduled Tasks）提权

- [ ] schtasks /query /fo LIST /v

重点找：
- 以 SYSTEM/管理员跑的任务
- Action 指向可写脚本/可写目录
- 调用未写绝对路径的程序（可 PATH 劫持）

检查脚本/目录权限：
- [ ] icacls "C:\path\to\script.ps1"
- [ ] icacls "C:\path\to\folder"

---

## 4) 凭据与“明文密码”（最常见捷径）
### 4.1 常见配置文件搜密码
- [ ] dir /s /b C:\*.config C:\*.ini C:\*.xml C:\*.txt 2>nul
- [ ] findstr /si /m "password pass pwd user username token key secret" C:\*.config C:\*.ini C:\*.xml C:\*.txt 2>nul

重点目录：
- C:\inetpub\
- C:\xampp\
- C:\ProgramData\
- C:\Users\<user>\Desktop\
- C:\Users\<user>\Documents\

### 4.2 命令历史/PS 历史

- [ ] type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt 2>nul

### 4.3 Windows 自带“保存的凭据”
- [ ] cmdkey /list

---

## 5) 权限组/特权（看到就兴奋）

### 5.1 SeImpersonatePrivilege

- [ ] whoami /priv

如果看到 SeImpersonatePrivilege=Enabled：
- 这通常意味着存在“令牌模拟”方向（实验室/OSCP 常见）
- 你要做的是：找可触发 SYSTEM 令牌的服务/组件路径（如某些 COM/服务交互场景）

### 5.2 Backup Operators / SeBackupPrivilege
- [ ] whoami /groups
- [ ] whoami /priv

命中后常见方向：
- 读取敏感文件（SAM/SYSTEM/SECURITY 等）→ 再做离线分析（靶场里常见链路）

---

## 6) 补充检查（经常捡漏）
- [ ] netstat -ano
- [ ] tasklist /svc
- [ ] dir /a C:\Users\*\Desktop 2>nul
- [ ] dir /a C:\Users\*\Documents 2>nul
- [ ] dir /a C:\Users\*\Downloads 2>nul

---

## 7) 工具加速（当参考，不要依赖）
- [ ] winPEAS（快速扫配置/权限/凭据）
- [ ] Seatbelt（安全项信息枚举）
- [ ] PowerUp（服务/路径/权限检查）

---

## ✅ OSCP 最常见“命中点”优先级
1) 服务权限错误（可写 service.exe / 可改服务配置）
2) 未加引号服务路径（Unquoted Service Path）
3) 计划任务跑可写脚本
4) 明文凭据（配置/脚本/历史）
5) 特权令牌（SeImpersonate/SeBackup 等）→ 走对应方向
6) 最后才考虑系统漏洞/内核类（耗时且风险高）

---

## 📌 每台机器复盘模板（10行足够）
- 入口：
- 当前用户/组：
- 关键服务/任务发现：
- 命中点证据（截图/命令输出）：
- 提权步骤摘要：
- 最终权限（whoami）：
- 修复建议一句话：