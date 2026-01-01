# impacket-getST

## 介绍

impacket-工作原理：我拿着一个“被信任的身份”，按Kerberos官方流程，向KDC要一个“替别人使用的服务票”

## 流程

### （1）S4U2Self（第一跳）

Client（你控制的账号）

 ↓

KDC：我这个服务，能不能“代表administrator”？

条件：（1）你控制的账号允许被委派，（2）目标资源配置了RBCD。

KDC返回：administrator->“你这个服务的”TGS

这一步：（1）不需要administrator密码（2）完全是Kerberos设计允许的

### （2）S4U2Proxy（第二跳）

Client（你控制的账号）

 ↓

KDC:我拿刚才的票，能不能“代表Administrator”去访问cifs/DC?

条件：（1）约束委派：SPN在允许列表里（2）RBCD:目标机器ACL允许你

KDC返回：administrator@cifs/DC的TGS

这张票=管理员访问DC的通行证

## 为什么这个流程能被滥用

因为Kerberos的设计假设是：“服务账号不会被攻击者控制”

但现实中：（1）服务账号密码弱（2）机器账号被拿下（3）ACL配错(RBCD)

信任模型被破坏，但协议依然合法

## getST vs ticketer

| 工具     | 原理                         |
| -------- | ---------------------------- |
| getST    | 向KDC申请真实TGS             |
| ticketer | 本地伪造TGT（Golden/Silver） |

