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