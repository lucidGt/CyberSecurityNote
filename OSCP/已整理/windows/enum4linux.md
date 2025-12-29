# enum4Linux

## 介绍

enum4linux常用来SMB/NetBIOS（Windows/Samba）信息枚举，尤其用来验证匿名（Null Session）能拿到什么信息，比如：域用户列表、密码策略、组成员关系等。

**快速枚举 SMB 主机信息**：主机名/域名/工作组、OS 信息、NetBIOS 信息

**枚举共享（shares）**：哪些共享可访问、是否允许匿名列出

**枚举用户/组**：列域用户、列域组、查组成员（有时能“绕”出来更全的用户列表）goadv2

**枚举密码策略**：锁定阈值、最小长度等（做喷洒/爆破前很关键）goadv2

**当匿名不可用时**：配合用户名/密码做“认证枚举”（信息更全）

### 核心“功能开关”

- `-a`：**all**，尽可能把常见枚举都跑一遍（最常用的一键）
- `-U`：枚举用户（users）
- `-G`：枚举组（groups）
- `-S`：枚举共享（shares）
- `-P`：枚举密码策略（password policy）
- `-o`：枚举 OS 信息（os info）
- `-r`：RID cycling（通过 RID 递增“猜”用户/组，环境允许时很强）
- `-R <start-end>`：配合 `-r` 指定 RID 范围（例如 `-R 500-550`）

### 认证/匿名相关

- `-u <user>`：指定用户名
- `-p <pass>`：指定密码
- `-d <domain>`：指定域/工作组
- `-n` / `-N`：无密码/空会话（null session，常用于匿名枚举）

## 你可以直接抄的几条命令

- **最省事（先跑一遍看能拿到啥）**
   `enum4linux -a <IP>`
- **只看共享**
   `enum4linux -S <IP>`
- **只看用户 + 密码策略**
   `enum4linux -U -P <IP>`
- **带凭据跑（信息通常更多）**
   `enum4linux -a -u 'USER' -p 'PASS' -d 'DOMAIN' <IP>`
- **RID 猜用户（环境允许时）**
   `enum4linux -r -R 500-1000 <IP>`