# RPC（Remote Procedure Call）

## 介绍

RPC = Remote Procedure Call

Remote -> 远程

Procedure -> 过程/函数/操作

Call -> 调用

## SCM（Service Control Manager）

用途：管理Windows服务

​	（1）创建/启动/停止/删除服务

​	（2）PsExec核心

典型RPC接口：

​	svcctl

什么时候想到它：

​	（1）有管理员

​	（2）想直接拿SYSTEM

​	（3）SMB/445通

PsExec = SMB + RPC（SCM）

## WMI（Windows Management Instrumentation）

用途：远程执行命令/查询系统

​	（1）执行进程

​	（2）查进程/服务/用户

​	（3）横向移动最常用

典型类：

​	（1）Win32_Process.Create

什么时候想到它：

​	（1）有凭据

​	（2）不想落地文件

​	（3）想安静执行命令

wmiexec = RPC（WMI）

## SAMR（Security Account Manager）

用途：本地/域用户与组信息

​	（1）枚举用户

​	（2）枚举组

​	（3）查RID

常见工具：

​	（1）rpcclient

​	（2）enumdomusers

什么时候想到它：

​	（1）枚举Windows/AD用户

​	（2）没拿到Shell之前的信息收集

## LSA/LSARPC

用途：安全策略&权限相关

​	（1）查本地策略

​	（2）查信任关系

​	（3）查SID

用法：

​	（1）枚举枚举

## NETLOGON

用途：域认证/域关系

​	（1）域成员<->DC通信

​	（2）域登录流程的一部分

用途：

​	（1）AD环境一定存在

## SRVSVC（Server Service）

用途：共享/会话相关

​	（1）枚举共享

​	（2）枚举连接会话

用途：

​	（1）SMB枚举背后

## ATSVC（Task Scheduler）

用途：计划任务

​	（1）创建/修改任务

​	（2）远程执行命令

用途：

​	（1）偶尔见

## DRSUAPI（域复制接口）

用途：

​	（1）域控复制数据

​	（2）DCSyanc用的

| 你想干嘛    | 实际用RPC服务 |      |
| ----------- | ------------- | ---- |
| 执行命令    | WMI           |      |
| 装/启动服务 | SCM           |      |
| 枚举用户    | SAMR          |      |
| 看域关系    | NETLOGON      |      |
| 共享枚举    | SRVSVC        |      |
| 计划任务    | ATSVC         |      |

