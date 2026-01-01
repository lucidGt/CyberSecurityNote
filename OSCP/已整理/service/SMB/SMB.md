# SMB(Server Manage Block)

## 介绍

端口：445/TCP

旧版本还可能是:139/TCP

系统：Windwos,部分Linux跑Samba

SMB=Windows版本的文件共享系统

## 提供线索

1）文件泄露

2）源码/配置泄露

3）凭据泄露

4）横向移动

5）有时候直接System

## 思考

1）能不能匿名枚举

2）有那些共享

3）共享能不能读文件

4）文件里有没有凭据、脚本

5）能不能用凭据登录别的服务

## 匿名/低权枚举

SMB允许匿名读取部分信息

共享名、用户名、目录结构、策略文件

## 读取共享文件

.ps1/.bat

config.xml

backup.zip

Groups.xml(GPP)

寻找明文密码、哈希、服务账号

## 横向移动（Windows、AD域）

一旦有凭据：

SMB登录其他机器

远程执行 

拷文件

探测本地管理员

## 历史漏洞

EternalBlue(MS17-010)

## 工具

### smbclient

枚举

smbclient -L //target_ip/ -N

-L 列共享

-N 匿名

进入共享

smbclient //target_ip/ -N

### smbmap(快速看权限)

smbmap -H targetIp

smbmap -H targetIp -u user -p pass

### enum4linux

enum4linux targetIp

### crackmapexec

crackmapexec smb targetIp

crackmapexec smb targetIp -u user -p pass

crackmapexec smb targetIp -u user -H hash

## 最小通过标准

会匿名枚举共享

会读共享里的文件

会找凭据、脚本、配置

会用SMB线索找下一个入口

## PsExec

1）身份认证+文件传输->SMB 445

通过445做这些事情

​	（1）NTLM/明文认证

​	（2）访问ADMIN$

​	（3）上传服务程序（exe）

​	（4）使用命名管道（Named Pipe）

👉 SMB本质工作

2）创建/启动/删除服务->RPC 135

​	（1）先连135/tcp

​	（2）135告诉你SCM在某个随机端口上

​	（3）客户端再连那个RPC高端口

​	（4）调用接口

​			①CreateService

​			②StartService

​	服务控制=RPC，不是SMB

3）命令执行

一旦服务被启动

​	（1）服务进程在目标机本地运行

​	（2）通常以SYSTEM权限运行

​	（3）不经过原先的网络端口

| 阶段        | 用到什么 | 端口        |
| ----------- | -------- | ----------- |
| 认证/传文件 | SMB      | 445         |
| 服务管理    | RPC/SCM  | 135->高端口 |
| 真正执行    | 本地服务 | 无          |

## PsExec和WNI对比

| 项目          | PsExec | WMI      |
| ------------- | ------ | -------- |
| 是否用SMB     | ✔      | ×        |
| 是否用RPC/135 | ✔      | ✔        |
| 是否创建服务  | ✔      | ×        |
| 是否写文件    | ✔      | ×        |
| 执行方式      | 服务   | 远程进程 |

