# DomainSid

## 介绍

DomainSID（域安全标识）是Active Direction域的“唯一指纹”，用于标识整个域的安全主体（用户、组、计算机等）

Domain Sid(Domain Security Identifier)域安全标识符

本质：一个唯一的字符串值，用来标识一个Active Directory域。

生成时机：域创建时随机生成（由Windows系统自动分配），终身不变。即使删除并重建域，也不会重复用旧的SID。

唯一性：在同一个域内（或森林内）绝对唯一，不同域的DomainSID不同（跨森林可能重复，但不影响安全）

## 主要作用

（1）构建域内所有对象的完整SID（Security Identifier）：完整的SID=Domain SID + RID（相对标识符）

（2）用于访问控制（ACL）、权限分配、Kerberos票据验证

（3）在Golden Ticket攻击中，必填参数（-domain-sid），伪造票据时必须正确，否则票据无效。

## SID结构（标准格式）

SID格式：S-1-5-21-A-B-C

（1）S-1：版本标识 （所有Windows SID以此开头）

（2）5：NT Authority （Windows安全权威）

（3）21：表示域或本地安全主体

（4）A-B-C：Domain Identifier（域唯一安全标识，随机生成的三组数字，例如 1088858960-373806567-254189436）。

（5）完整用户/组 SID：Domain SID + RID （RID如500为Administrator，512为Domain Admins）

示例（HTB Administrator 机器常见）：

Domain SID：S-1-5-21-1088858960-373806567-254189436

Administrator SID：S-1-5-21-1088858960-373806567-254189436-500

Domain Admins 组 SID：S-1-5-21-1088858960-373806567-254189436-512

## 利用

1）枚举Domain SID：

方式一：

Get-Domain | Select DomainSID

方式二：

impacket-lookupsid domain/user:pass@ip

2）Golden Ticket 生成（必须用正确 Domain SID）：

python3 ticketer.py -nthash krbtgt哈希 -domain-sid S-1-5-21-... -domain corp.local -user-id 500 administrator

注意：常见坑：SID 错误会导致票据无效；克隆机器未 sysprep 会导致机器 SID 重复（加入域失败）。