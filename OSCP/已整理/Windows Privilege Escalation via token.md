# Windows Privilege Escalation Via Token



## SelmpersonatePrivilege

### 1）介绍

允许你把别人给你的模拟令牌（Impersonation Token）套在我的线程上假装身份干活。

### 2）为什么能够提取？

Windows服务里很多高权限服务(SYSTEM)会通过命名管道、COM、RPC等机制跟低权限进程交互。

如果能够诱导一个SYSTEM服务链接到我控制的端点，就能拿到它的Token，实现提升权限。

### 3）常见利用套路

Potato系列（JuicyPotato、RoguePotato、GodPotato等）：利用COM、RPC体系让SYSTEM来连你，然后你impersonate这个SYSTEM token。

PrintSpoofer：利用打印相关服务的交互方式，拿到SYSTEM token后Impersonate

### 4）常见前提、限制

（1）SeImpersonatePrivilege Enabled

（2）环境要满足对应的技术点（OS版本、服务是否可用、补丁情况、Token类型、完整性级别）

（3）当前进程通常是某类服务账号（IIS的app pool、服务账号）

### 5）常见失败原因

（1）目标系统补丁、策略导致那条诱导链断了

（2）DCOM、RPC、打印服务相关组件被禁用或限制

（3）拿到的是不能用于创建进程的Token类型

### 6）防守、加固

（1）最小化权限：不给不需要的用户SeImpersonatePrivilege

（2）收紧DCOM、RPC、打印服务相关组件

（3）及时补丁

## SeAssignPrimaryToken

### 1）介绍

允许你把一个Token设置成新进程的Primary Token（主令牌）

跟SeImpersonate的差别是

（1）Impersonate：像临时借用身份

（2）AssignPrimaryToken：像给新进程换身份证（整个进程存活周期都能用）

### 2）为什么能提取

如果能拿到一个高权限的Token（SYSTEM的Primary Token），那就能创建一个真正以SYSTEM身份启动的进程。

### 3）常见利用套路

（1）通常它会和”能获取SYSTEM token“的方式搭配（同样可能走RPC、服务交互、漏洞链）

（2）或者配合某些服务配置错误（服务以SYSTEM跑、但你能影响它生成、传递Token的过程）

#### 4）常见前提、限制

（1）这个特权比SeImpersonate更少见

（2）还需要拿到高权限的Primary Token这个环节

## SeDebugPrivilege

### 1）介绍

允许你以调试、打开其他进程（包括高权限进程）的剧情，读取、写入他们的内存

### 2）为什么能够提权

（1）读敏感进程拿凭据、密钥、

最典型是读取认证相关进程内存（LSASS）

一旦拿到高权限凭据、哈希、票据，下一步就是给横向或本地提权

（2）对高权限进程做注入、劫持

通过向SYSTEM进程注入线程、代码，让它帮你执行

### 3）常见前提、限制

（1）得真的拥有进程并且启动SeDebugPrivilege

（2）现代Windows有更多保护机制（例如对敏感进程 额外保护、凭据隔离等）会让直接读变困难

### 4）防守、加固

（1）限制谁拥有SeDebugPrivilege（默认一般指给管理员、特定组）

（2）开启更多凭据保护、减少明文、减少可导出秘密

（3）监控对敏感进程的异常句柄访问行为

## 快速决策

whoami /priv

### 看到SeImpresonatePrivilege Enabled

考虑能不能够通过服务交互拿到SYSTEM TOKEN->ImPresonate->出SYSTEM

### 看到SeAssignPrimaryToken Enabled

考虑能不能拿到高权限的primary Token->直接启动SYSTEM进程

### 看到SeDebugPrivilege Enabled

考虑能不能从高进程提取出可复用的凭据、密码->横向出管理员、SYSTEM



## 什么是Potato（SeImpresonatePrivilege利用）

### 介绍

最早的利用方法名字里带了JuicyPotato，后来不断变种，安全圈就把这类同源Token提取技术叫做Potato系列。

### windows技术的设计特点

SYSTEM服务经常会通过RPC、COM、命名管道去连接低权限进程。

（1）满足有SeImpersonatePrivilege

（2）能让SYSTEM连接你

那么就可以：

（3）拿到SYSTEM的Impersonation Token->变成SYSTEM

### 攻击链

【低权限进程】

->【制造一个"SYSTEM 会来链接你的 场景"】

->【SYSTEM服务链接你控制的端点】

->【WINDOWS自动会给你一个SYSTEM的impersonate Token】

->【你用SeImpersonatePrivilege套上这个Token】

->【达到SYSTEM】

关键点：不是你去抢SYSTEM，是SYSTEM来找你

### JuicyPotato

（1）依赖DCOM、COM

（2）新系统很多不行了

JuicyPotato.exe

### RoguePotato

（1）绕过部分JuicyPotato的限制

（2）仍然是DCOM、RPC思路

可行性环境：

RPC状态

1）查看RPC服务

sc query RpcSs

2）RPC端口

netstat -ano | findstr 135

DCOM状态

1） DCOM 是否启用

reg query HKLM\Software\Microsoft\Ole /v EnableDCOM

2）DCOM服务状态

sc query DcomLaunch

端点状态：

1）命名管道

dir \\.\pipe\

2）端点状态

dir \\.\pipe\ | findstr spool

RoguePotato.exe

### PrintSpoofer

（1）利用打印相关服务

（2）命中率高

（3）在很多Server、桌面版都能用

可行性环境：

1）打印机服务  

sc query spooler

sc qc spooler

看目标石否DC

systeminfo | findstr /i "Domain"

2）Token本身是否可用起进程

whoami /all

EnableLUA

ConsentPromptBehaviorAdmin

LocalAccountTokenFilterPolicy

3）执行是否被拦（AppLocker、WDAC、Defender、SRP）

4）SeImpersonate

PrintSpoofer -i -c 'commond'

### GodPotato

（1）更新的实现

（2）对新系统友好

（3）本质仍是Token Impersonation

GodPotato.exe

## SedebugPrivilege利用

1）读取高权限进程内存

2）操作、复制高权限Token

3）注入代码到高权限进程

一般拥有SedebugPrivilege权限 = 可用读LSASS这类进程

### 相关工具

| 工具                            | 用途                         |      |
| ------------------------------- | ---------------------------- | ---- |
| Mimikatz                        | 从高权限内存中提取凭据、票据 |      |
| ProcDump                        | 导出进程内存                 |      |
| Task Manager、Debug Api（思路） | 打开SYSTEM进程               |      |

### Token操作、进程注入

| 工具               | 用途                     |      |
| ------------------ | ------------------------ | ---- |
| Token Manipulation | 从SYSTEM进程复制Token    |      |
| 进程注入类工具     | 让SYSTEM进程替你执行命令 |      |
| 自定义POC          | API级别操作              |      |

