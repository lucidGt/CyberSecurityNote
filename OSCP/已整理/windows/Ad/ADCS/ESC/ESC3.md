# ESC3

## 介绍

ESC3攻击场景的核心组件（OID:1.3.6.1.4.1.311.20.2.1），利用Certificate Request Agent字段。

## Certificate Request Agent是什么？

### 介绍

Certificate Request Agent EKU（Extended Key Usage扩展），也叫做Enrollment Agent（注册代理），

### 设计目的

微软合法功能，用于委托注册（Enrollment On Behalf Of）：持有该Eku的证书可以代表其他用户（包括域管）请求任意模板的证书。（常见于智能卡发行、帮助台代理用户注册）

## 它不是漏洞。而是滥用形成ESC3漏洞

### ESC3漏洞本质

​	（1）当证书模板误配置（低权限用户可注册+包括Certificate Request Agent EKU + 无代理限制）时，攻击者得到“代理证书”

​	（2）用代理证书on-behalf-of请求其他模板（如User，有Client Authenticate EKU）的证书，伪造成任意用户（包括administrator）

​	（3）结果：域提权（获取admin认证证书）

### 1）当证书模板误配置 无代理限制（默认无限制）

​	CA级限制：管理员可在CA属性（certsrv.msc->Enrollment Agents标签）配置Enrollment Agent Restrictions

​	（限制代理用户）（限制模板）（默认无限制）

​	模板级限制：模板模板可要求Manager Approval（经理批准）或者Authorized Signatures（授权签名），代理也许满足

### 使用条件

（1）至少两个模板：一个提供代理EKU（低权限可注册），另一个有认证EKU（允许代理请求）

（2）无Enrollment Agent Restrictions （代理限制，默认无）

### 为什么危险

（1）绕过目标模板Enrollment权限检查，代理“万能”

## 为什么Certificate Request Agent能绕过Enrollment权限检查

### 介绍

这是ADCS的合法设计机制（Enrollment on Behalf of，委托注册），CA在处理代理请求时，只验证代理证书的有效性（是否有Certificate  Request Agent EKU），不检查被代理用户的（on-behalf-of的目标用户）对目标模板的Enrollment权限。这在误配置环境下滥用形成ESC3漏洞。

### 正常请求

用户直接请求模板证书->CA检查请求者是否有该模板Enrollment权限（Enrollment Rights ACL）

### 代理请求（on-behalf-of）

1）请求包含代理证书（有Certificate Request Agent EKU，OID:1.3.6.1.4.1.311.20.2.1）

2）CA验证是否有效

​	（1）代理证书签名是否有效

​	（2）代理证书有Certificate Request Agent EKU。

​	（3）（可选）CA配置的Enrollment Agent Restrictions（默认无限制）

3）关键绕过：CA不检查被代理用户（如administrator）是否有目标目标（如User）的Enroll权限，直接办法证书给代理者。

## 利用

```
1）提交Certificate Request Agent
certipy-ad req -ns '10.129.232.167' -dc-ip '10.129.232.167' -u 'cert_admin' -p 'aA12345677..' -template 'user' -ca 'tombwatcher-CA-1' -on-behalf-of 'tombwatcher\administrator' -pfx 'cert_admin.pfx'
2）提交TGT
certipy-ad auth -ns 10.129.232.167 -dc-ip 10.129.232.167 -domain 'tombwatcher.htb' -pfx 'administrator.pfx'
```

