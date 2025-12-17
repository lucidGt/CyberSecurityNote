# Windows Scheduled Task

## 介绍

Windows计划任务（Scheduled Task）=系统按”时间/事件/启动/登录“自动执行程序或脚本的机制

也就是一个定时的脚本

## 为什么能够提权

高权限允许+可控执行内容=提权

1）任务用SYSTEM/Admistrator跑

2）它执行的exe/bat/ps1/cmd

3）那个文件或目标你能写

等任务一触发，你的代码就以高权限执行

## 计划任务有那些“触发方式”

### 1）定时触发（Time-based）

每1分钟

每5分钟

每天凌晨

最值钱的一类

（1）不需要重启电脑

（2）不需要管理员操作

（3）等就行

### 2）开机触发（At startup）

（1）系统启动时执行

（2）几乎一定是SYSTEM

触发方式：

（1）重启机器

### 3）登录触发（At logon）

（1）某用户登录时执行

（2）可能是：

​		①任意用户

​		②指定用户（管理员）

如果是管理员登录高价值

有时候等不到，试试手动run

### 4）事件触发（On event）

（1）某个事件发生才执行

​		①服务启动

​		②特定错误日志

## 计划任务里“执行什么”

计划任务执行的不是任务本身而是Action：

常见Action类型：

（1）.exe

（2）.bat

（3）.cmd

（4）.ps1

永远要问：这个Action指向的文件我能不能改？

## 怎么枚举计划任务

### （1）全量枚举

schtasks /query /fo LIST /v

/query 查询

/fo LIST 以LIST格式输出

/v 详细信息

### （2）盯着三个数据看

①Run As User：用谁的权限跑

②Task To Run/Actions：执行什么

③Triggers：什么时候跑

### （3）对可疑路径查权限

icacls "xx"

只要看到：

①User

②Authenticated Users

③有W/N/F

直接列为可用

## 判断值不值得打

（1）SYSTEM/ADMIN跑吗

（2）执行的是文件还是命令（文件看能不能改写，命令看能不能改配置）

（3）路径我能写吗？

（4）我能不能触发？