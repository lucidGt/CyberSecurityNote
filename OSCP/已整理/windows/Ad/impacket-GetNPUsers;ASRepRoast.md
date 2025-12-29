# ASRepRoast

## 介绍

AS-Rep是Kerberos认证阶段中，域控（KDC）返回给客户端的“认证响应包”用来证明用户身份，并向客户端发放TGT(Ticket Granting Ticket)。

AS-REP
	├── Session Key（会话密钥）
	│     └─ 用【用户密码 / NT hash】加密
	│
	└── TGT（Ticket Granting Ticket）
      	└─ 用【krbtgt 账户的密钥】加密

Active Directory开启了UF_DONT_REQUIRE_PREAUTH，就会有AS-REP包。

通过暴力破解AS-REP中的Session Key就能得到用户NT Hash。

## ASRepRoast利用工具

### 测试枚举

impacket-GetNPUsers intelligence.htb/ -usersfile users.txt -no-pass

### BloodHound/PowerView

Get-DomainUser -PreauthNotRequired

## 存在的原因

（1）早期Kerberos兼容性

（2）某些旧设备/旧账号

（3）管理员误操作

## 存在的前提

1）UF_DONT_REQUIRE_PREAUTH

​	（1）关闭kerberos预验证

​	（2）AS-RepRoasting前提

2）不需要凭据

3）离线爆破

4）比kerberoast更白给