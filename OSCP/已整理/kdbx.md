# KDBX

## 介绍

KDBX是一种加密密码数据库的文件格式，最常见KeePass/KeePassXC密码管理器。

KDBX的基本信息

| 项目       | 说明                     |
| ---------- | ------------------------ |
| 文件后缀   | .kdbx                    |
| 常用软件   | KeePass、KeePassXC       |
| 加密算法   | AES-256/ChaCha20         |
| 完整性校验 | HMAC-SHA256              |
| 解锁方式   | 主密码/Key file/二者同时 |
| 平台       | Windows/Linux/MacOS      |

分层加密

1.主密码（Master Key）

​	（1）来自主密码+Key file

​	（2）经过大量Key Derivation防暴力

2.数据库整体加密

​	（1）所有条目（账号/密码）都在密文里

3.内存保护

​	（1）解锁后，密码字段仍尽量避免明文驻留

## KDBX利用

### 1）常见位置

/Desktop,/Documents,/Downloads，共享目录，备份文件夹,GIT仓库

搜索 find / -iname "*.kdbx" 2>/dev/null

### 2）一旦拿到KDBX，下一步

#### 	A）有主密码

​	keepassxc database.kdbx

​	有可能能拿到（1）域用户密码（2）管理员账号（3）VPN/SSH凭据

#### 	B）没有主密码

​	进入离线字典爆破流程

​	keepass2john xxx.kdbx > kdbx.hash

​	hashcat -m 13400 kdbx.hash rockyou.txt

### 3）kpcli读取

## 为什么KDBX在真实环境很常见

（1）域管理员密码存在KeePass

（2）把所有服务器凭据集中管理

（3）把KDBX文件放在低权用户读到的地方

问题：（1）弱主密码（2）文件权限（3）密码复用

