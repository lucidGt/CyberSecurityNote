# Registry

## 介绍

Registry（注册表）就是Windows配置数据库。很多程序/服务会把

（1）配置路径

（2）启动项

（3）服务参数

（4）（有时）凭据

写进注册表

## 常用的6类注册表枚举目标

### A.自动登录凭据（AutoLogon）

很多真实环境会配置自动登录，密码可能以明文的方式或可逆的形式出现。

查键：

HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon

常见字段：

（1）AutoAdminLogon

（2）DefaultUserName

（3）DefaultDomainName

（4）DefaultPassword

命令：

reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName
	reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword

### B.启动项（Run/RunOnce）

用来找：高权限启动但路径可写或者隐藏的脚本

查键：

HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce

HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

命令：

reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
	reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

### C.AlwaysInstallElevated（MSI提权配置）

必须同时开启的前提下才能使用，低权用户也能通过MSI提权。

两个位置：

HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer

HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer

命令：

reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
	reg query "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated

### D.已保存的远程记录连接痕迹（RDP）

用来找主机名、用户名

查键：

HKCU\Software\Microsoft\Terminal Server Client\Servers

命令：

reg query "HKCU\Software\Microsoft\Terminal Server Client\Servers" /s

### E:PowerShell历史路径（配合找凭据）

注册表不一定存历史，但常用做法是直接读历史文件；可用把它当成凭据来源的必查

(Get-PSReadlineOption).HistorySavePath

找关键词：password,credential,net use,Enter-PSSession等

### F.应用程序配置（第三方软件）

检查：HKLM\Software\或者HKCU\Software\存配置

命令：

reg query "HKLM\SOFTWARE" /s | findstr /i "pass pwd credential user login key token"
	reg query "HKCU\SOFTWARE" /s | findstr /i "pass pwd credential user login key token"

## 看注册表输出的思路

高价值目标：

1.用户名/域名/密码字段（DefaultPassword/Password/Pwd/Credential）

2.可执行路径（可是不是指向可写目录）

3.策略配置（AlwayInstallElevated/禁用UAC等）

## 建议

拿到Windows Shell后

1.Winlogon（AutoLogon）

2.Run/RunOnce（启动项）

3.AlwayInstallElevated

4.第三方软件配置

