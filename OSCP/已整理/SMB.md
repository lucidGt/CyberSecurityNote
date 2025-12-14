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