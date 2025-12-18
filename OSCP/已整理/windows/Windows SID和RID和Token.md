# Windows SID和RID和Token

## SID

常见SID格式：S-1-5-21-3623811015-3361044348-30300820-1013

| 部分                           | 含义                     |
| ------------------------------ | ------------------------ |
| S                              | Security Identifier      |
| 1                              | SID版本                  |
| 5                              | 授权机构（NT authority） |
| 21                             | 本地机器或域             |
| 3623811015-3361044348-30300820 | 机器、域唯一ID           |
| 1013                           | RID（相对标识符）        |

## RID

常见RID

| RID   | 含义                      |
| ----- | ------------------------- |
| 500   | Administarotr(内置管理员) |
| 501   | Guest                     |
| 502   | KRBTGT(域)                |
| 512   | Domain Admins             |
| 513   | Domain Users              |
| 544   | 本地Administrators组      |
| 1000+ | 普通用户                  |

### 通过RIP判断管理员

## 为什么删用户重建，权限还在/不在

删除用户->SID消失

新建同名用户->新SID

用户名相同、权限不同

## SID在权限里的用途

### 1）文件/注册表ACL

Allow S-1-5-21-...-500

而不是

Allow Administrator

相当于SID是主键

### 2）Token里装的是什么

当登录后，access token里包含

1）用户SID

2）所属组SID

3）特权（SeImpresonate等）

Token=SID集合+特权

## 一些判断

### 判断是否管理员

whoami /groups

S-1-5-32-544

这就是Administrators组的SID

### 判断域vs本地用户

whoami /user

S-1-5-21-<域ID>-<RID>->域用户

S-1-5-21-<机器ID>-<RID>->本地用户

## Windows跟Linux比较

Linux看UID、GID 

Windows看SID、RID

## 为什么Windows不直接用用户名

用户名：不安全、不唯一、不稳定

Windows判断 权限时，只看两个问题

1）这个Token里有没有某个SID?

2）这个Token里有没有某个特权？

有->放行 没有->拒绝

## Token拆出来看

### Token = SID(SID+GroupSID) + Privileges

### SID集合

1）用户SID

2）组SID(Administrators/Domain Users/Everyone) [列表]

### 特权（Privileges）

这个特权不是文件权限，而是系统动作权限。

不通过ACL控制，直接挂在Token上



## Token保存在哪里？

Token是一个内核对象（Kernel Object） 只存在于内存中

## 如何生成Token

### 1）用户登录（认证）

用户名、密码/NTLM/Kerberos凭据

Windows会把这些交给LSA（Local Security Authority）

### 2）LSA验证你是谁

LSA会：

1）验证凭据是否正确

2）查SAM（本地）或AD（域）

3）找到你的用户SID

4）找到你所属的所有组SID

5）查你所拥有的而特权（Privileges）

这一步还没有Token，只是调查你是谁？

### 3）LSA创建Access Token (核心)

验证后,LSA会在内核里创建一个Access Token对象

这个内核对象包含：

1）用户SID

2）组SID集合

3）Privileges

4）完整性级别（Integrity Level)

5）Token类型（Primary / Impresonation）

6）一些安全标志

### 4）将Token绑定到第一个进程

Token不会单独存在，它会立刻被：

1）绑定到你的登录进程

之后：

每一个你启动的进程，都会“继承”一个Token

##### 5）随着进程结束释放Token

进程结束->Token释放->垃圾回收

## 为什么一个用户拥有多个Token？

Token是进程级，不是用户级的

所以：

1）一个用户

2）可用同时拥有多个Token

3）每个Token绑定到进程

4）用户SID一样

5）但特权、完整性级别、是否受限可能不一样

## UAC为什么能够限制管理员

LSA会给同一个用户创建两个Token

1）一个受限Token（去掉管理员SID）

2）一个完整Token（保留管理员SID）

3）默认进程用的是受限Token

## 提权到底在干什么？

1.让系统重新生成Token（重新登录、服务启动）

2.借用别人的Token(SeImpersonate)

3.复制/操作Token（SeDebug/SeAssignPrimaryToken）

4.让进程继承一个更强的Token