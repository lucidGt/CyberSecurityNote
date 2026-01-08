# net rcp

## 介绍

net是Samba工具包中的一个多功能命令行工具，常通过RPC（Remote Procedure Call）针对Windows系统进行远程管理。

## 通用参数

| 参数                     | 说明                          | 常见用法                                           | 注意事项         |
| ------------------------ | ----------------------------- | -------------------------------------------------- | ---------------- |
| -I \<TARGET_IP\>         | 直接指定目标IP（避免DNS问题） | net rpc shutdown -I 10.10.10.100 ...               |                  |
| -S \<TARGET\>            | 指定目标主机名或IP            | net rpc user -S WIN-PC ...                         | 需要主机名能解析 |
| -U \<USERNAME\>%PASSWORD | 指定凭证（用户名%密码）       | -U "administrator%pass123" 或 -U "" (null session) | 空密码用 ""      |
| -W \<DOMAIN\>            | 指定域或工作组                | -W CORP                                            | 默认本地工作组   |
| -f                       | 强制操作（常用于shutdown）    | net rpc shutdown -f ...                            | 强制关闭应用     |
| -r                       | 重启（需结合-f）              | net rpc shutdown -r -f ...                         |                  |
| -t                       | 延迟秒数（默认20）            | -t 0（立即执行）                                   | shutdown 常用    |
| -C "MESSAGE"             | 关机时显示自定义消息          | -C "System maintenance"                            |                  |
| -d \<LEVEL\>             | 调试级别（0-10）10最详细      | -d 10（排查错误）                                  | 报错时用         |
| -p \<PORT\>              | 指定端口（默认先445，再139）  | 很少用                                             |                  |
| --request-timeout        | 请求超时设置                  | 网络慢时用                                         |                  |

## 常用子命令表格

| 子命令               | 功能                             | 常见用法                                                     | 场景                           |
| -------------------- | -------------------------------- | ------------------------------------------------------------ | ------------------------------ |
| shutdown             | 关机                             | net rpc shutdown -I 10.10.10.100 -U admin%pass -f -t 0       | 获得高权限后干扰目标或测试权限 |
| abortshutdown        | 取消关机                         | net rpc abortshutdown -I IP -U admin%pass                    |                                |
| user                 | 列出/管理用户                    | net rpc user -I IP -U ""（匿名列用户）net rpc user add newuser pass -I IP -U admin%pass | 枚举用户、创建后门账户         |
| user delete \<USER\> | 删除用户                         |                                                              |                                |
| group                | 列出/管理组                      | net rpc group members "Domain Admins" -I IP -U admin%pass    | 枚举域管组成员                 |
| group admin          | 添加组成员                       | net rpc group addmem "Domain Admins" user -I IP -U admin%pass | 横向移动后加后门               |
| share                | 列出/管理共享                    | net rpc share -I IP -U user%pass                             | 枚举共享目录                   |
| rights               | 授予系统权限（如添加计算机账户） | net rpc rights grant "DOMAIN\user" SeMachineAccountPrivilege -I IP -U admin%pass | RBCD 等高级提权链              |
| info                 | 显示目标基本信息                 | net rpc info -I IP -U user%pass                              | 快速确认域信息                 |

## 注意

### 1）Null Session 尝试：很多旧机器支持匿名，优先试 -U "" 枚举用户/共享。

### 2）常见错误处理：

NT_STATUS_ACCESS_DENIED → 凭证错误或权限不足。

连接失败 → 检查 135/139/445 端口，现代 Windows 可能禁用 RPC。

### 3）与其它工具对比：

rpcclient：交互式，更详细枚举（enumdomusers 等）。

smbclient：文件传输。

crackmapexec / enum4linux：自动化枚举后，再用 net rpc 精细操作。