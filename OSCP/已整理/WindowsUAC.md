# WindowsUAC

## 介绍

Windows UAC = Windows User Account Control，用户账户控制，是Windows防止未经授权的系统级操作的安全机制。

| 项目          | 含义                   |
| ------------- | ---------------------- |
| Administrator | 你有没有管理员权限     |
| UAC           | 你用不用的上管理员权限 |

## UAC在干嘛？

UAC的作用：

​	（1）把管理员的账号拆成两层

​		①普通权限（默认）

​		②高完整性权限（需要确认）

​	（2）UAC配置不当本质

​		①系统错误的允许你自动升高（无需确认）

## 有价值的UAC配置不当

### （1）Admin Approval Mode 关闭

EnableLUA 配置错误

管理员账号不需要UAC确认就能以高权限运行程序。

判断方法

reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA

EnableLUA = 0 -> UAC关闭

### （2）UAC等级过低（自动提升）

ConsentPromptBehaviorAdmin 配置错误

 管理员执行程序，不需要确认框，直接提升。

判断方法

reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin

ConsentPromptBehaviorAdmin = 0 -> 管理员执行程序，不需要确认框，直接提升。

### （3）AlwayNotify关闭+自动提升白名单程序

机制

Windows有一批”自动提升”的系统程序

​	①fodhelper.exe

​	②computerdefaults.exe

​	③eventvwr.exe

在UAC配置不严格时：

​	①这些程序自动以高完整性运行

​	②它们会读取用户可控的注册表键

配置不当+自动提升=可利用

### （4）可写UAC相关注册表键（配合使用）

例子

HKCU\Software\Classes\ms-settings\Shell\Open\command

如果：

​	①UAC不是最高等级

​	②你是本地管理员

​	③这些键你能写

​	启动auto-elevated程序->执行你的命令

## 什么时候考虑UAC？

（1）我已经是管理员了

（2）但

​	执行某些命令被拦、

​	权限不是SYSTEM/高完整性

否则

直接用服务/计划任务/凭据

## 判断流程

我是不是管理员？
	 ├─ 否 → 不看 UAC
	 └─ 是
 	    ↓
EnableLUA / ConsentPromptBehaviorAdmin？
	 ├─ 配置宽松 → 直接高权限
	 └─ 正常
   	  ↓
有没有自动提升程序 + 可写注册表？
	 ├─ 有 → 可试
	 └─ 没有 → 放弃