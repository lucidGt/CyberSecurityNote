# SNMP(Simple Network Management protocol)

## 介绍

端口：161UDP

用途：让管理员查看设备状态

对象：服务端、路由器、交换机

通过SNMP可能拿到：

操作系统版本

主机名

本地用户

正在运行的进程

脚本路径、定时任务线索

内网IP、网络结构

## 工具

### snmpwalk

snmpwalk -v2c -c public targetIp

## 关键词

#### 用户

user、login、account

思考：SSH、SMB其他服务

#### 进程

process、running、python、java、bash

思考：cron、服务、提权点

#### 路径

/opt/、/usr/local/、/var/www/、/home/

思考：ls -l 检查权限

#### 脚本

backup、script、.sh、.py、.pl

思考：是否被root定时执行

#### 服务

service、daemon、sshd、cron、apache、mysql

思考：定向枚举对应服务

#### 端口

port、listen、127.0.0.1

思考：SSH转发、本地提权后访问

#### 操作系统

Linux、Ubuntu、Debian、Kernel

思考：uname -a对照

#### 网络

interface、ip、eth0、ens33、10.0、192.168

思考：横向移动/内网扫描

#### 配置

config、.conf、.cfg、settings

思考：登录后第一时间找到对应文件

#### 明文参数

password、passwd、secret、key、token

思考：SSH、数据库、WEB、横向

