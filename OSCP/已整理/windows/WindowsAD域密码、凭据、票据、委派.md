# NTLM-NTLMV2

## NTLM

客户端直接用NTLM Hash加密明文,NTLM Hash=长期凭证。

（1）可以抓到NTLM Hash

（2）NTLM Hash离线爆破密码明文

（3）可以Pass The Hash

（4）可以中继Relay

## NTLMV2

客户端使用服务器Challenge加密

改变核心：不再直接使用NtlmHash加密，先使用：服务器Challenge、时间戳、目标信息加密成NTLMv2 Response

（1）可以结合Challenge离线爆破

（2）可以中继Relay

## 防御角度

| 防护            | 作用     |
| --------------- | -------- |
| 禁用NTLM        | 根本解决 |
| SMB Signing     | 防Relay  |
| LDAP Signing    | 防Relay  |
| Channel Binding | 防Relay  |
| 强制Kerberos    | 最优     |

# 委派（Delegation）

## 非约束委派（Unconstrained Delegation）

### 介绍

允许一个服务/机器，代表用户访问“任意服务”

### 关键属性

AD属性：TrustedForDelegation

KDC行为：（1）用户访问该服务（2）把用户的可转发TGT交给服务

服务内存会缓冲用户TGT

### 流程

用户->委派服务

KDC->给TGS+用户TGT

服务->可用该TGT访问任意服务

## 约束委派（Constarined Delagation,KCD)

### 介绍

允许服务代表用户，但只能访问指定服务。

限制：能去哪

### 关键属性

AD属性：msDS-AllowedToDelegateTo

配置对象：委派者账号（机器账号，服务账号）

内容：SPN白名单

### 流程

服务->KDC(S4U2Self)

服务->KDC(S4U2Proxy)

KDC：检查AllowedToDelegateTo是否包含目标SPN

->给User->TargetSPN的TGS

## 资源约束委派（Resource-Based Constrained Delegation,RBCD）

### 介绍

由“目标资源”决定，谁可以代表用户访问我。

限制：谁能来

### 关键属性

AD属性：msDS-AllowedToActOnBehalfOfOtherIdentity

配置对象：目标机器账号

内容：账号ACL（谁被允许冒充）

不使用SPN列表

### 流程

我（服务/机器） → KDC（S4U2Self）
	我 → KDC（S4U2Proxy，目标 SPN）
	KDC：检查目标机器的 RBCD ACL 里是否有我
	→ 给 User → TargetSPN 的 TGS