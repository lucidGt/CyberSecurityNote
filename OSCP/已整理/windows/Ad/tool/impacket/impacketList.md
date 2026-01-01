# impacket-list

## 功能介绍

| 脚本名称       | 主要功能                                      | OSCP 常见应用场景               | 示例命令（简化）                                 |
| -------------- | --------------------------------------------- | ------------------------------- | ------------------------------------------------ |
| psexec.py      | PSEXEC 风格远程命令执行（上传服务获取 shell） | 横向移动、获取 SYSTEM shell     | impacket-psexec domain/user:pass@target          |
| wmiexec.py     | 通过 WMI 执行半交互 shell                     | 隐蔽横向移动（无文件落地）      | impacket-wmiexec domain/user:pass@target         |
| smbexec.py     | 通过 SMB 执行半交互 shell                     | 横向移动（日志少）              | impacket-smbexec domain/user:pass@target         |
| atexec.py      | 通过任务计划执行命令                          | 横向移动                        | impacket-atexec domain/user:pass@target cmd      |
| dcomexec.py    | 通过 DCOM 执行半交互 shell                    | 横向移动（绕过某些限制）        | impacket-dcomexec domain/user:pass@target        |
| secretsdump.py | 远程转储 SAM/LSA/NTDS 哈希（包括 DCSync）     | 凭据转储、域哈希 dump           | impacket-secretsdump domain/user:pass@DC         |
| GetNPUsers.py  | AS-REP Roasting（获取无预认证用户哈希）       | Kerberos 攻击、离线破解         | impacket-GetNPUsers domain/ -usersfile users.txt |
| GetUserSPNs.py | Kerberoasting（获取有 SPN 用户 TGS 哈希）     | Kerberos 攻击、离线破解服务账户 | impacket-GetUserSPNs domain/user:pass -request   |
| ticketer.py    | 生成 Golden/Silver Ticket                     | 持久化、域完全控制              | impacket-ticketer -nthash krbtgt_hash ...        |
| ntlmrelayx.py  | NTLM 中继攻击（继电器认证到其他服务）         | 中继到 LDAP/SMB、权限提升       | impacket-ntlmrelayx -t ldap://DC -smb2support    |
| smbclient.py   | SMB 客户端（浏览/上传/下载文件）              | 文件传输、共享枚举              | impacket-smbclient domain/user:pass@target       |
| smbserver.py   | 简单 SMB 服务器（文件共享/哈希捕获）          | 文件传输、NTLM 哈希捕获         | impacket-smbserver share . -smb2support          |
| samrdump.py    | 通过 SAMR 枚举用户/共享信息                   | 域枚举                          | impacket-samrdump target                         |
| lookupsid.py   | SID 爆破枚举用户/组                           | 域枚举                          | impacket-lookupsid domain/user:pass@target       |
| reg.py         | 远程注册表操作（读写）                        | 持久化、配置修改                | impacket-reg target save ...                     |
| services.py    | 远程服务管理（启动/停止/创建）                | 横向/持久化                     | impacket-services target start ...               |
| rpcdump.py     | 枚举 MSRPC 端点                               | 服务枚举                        | impacket-rpcdump target                          |
| netview.py     | 枚举域会话/登录用户                           | 域枚举、横向目标发现            | impacket-netview domain/user:pass                |