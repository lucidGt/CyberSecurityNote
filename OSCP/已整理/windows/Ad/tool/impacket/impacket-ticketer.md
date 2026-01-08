# impacket-ticketer

## 介绍

impacket-ticketer = 离线伪造Kerberos票据的工具

impacket-ticketer是专门用来伪造Kerberos票据（Ticket）工具，核心用途就是制造Golden Ticket/Silver Ticket，配合Pass-the-Ticket（PTT）使用，在AD环境里实现长期、隐蔽、高权限访问。

（1）不和DC通信

（2）不校验密码是否真实

（3）只要关键密钥在手，自己就能签发合法票据。

## Kerberos里它在干什么？

Kerberos票据本质是DC用密钥签名的数据结构：

​	（1）TGS：由krbtgt账户签名

​	（2）TGS：由具体服务账户签名（CIFS、HTTP、MYSQL）

Ticketer就是伪造并签名这些票据

## 参数

| 参数        | 说明                                  | 示例值                                  | 场景                      |
| ----------- | ------------------------------------- | --------------------------------------- | ------------------------- |
| -nthash     | NTLM哈希（推荐）                      | 1181ba47d45fa2c76385a82409cbfaf6        | Golden/Silver Ticket 生成 |
| -hashes     | LM:NTHASH（兼容旧系统）               | aad3b435b51404ee...:1181ba47...         | 很少用                    |
| -domain-sid | 域 SID（必填）                        | S-1-5-21-1088858960-373806567-254189436 | 所有票据生成              |
| -domain     | 域 FQDN                               | administrator.htb                       | 必填                      |
| -user-id    | 用户 RID（默认 500 为 Administrator） | 500                                     | Golden Ticket             |
| -extra-sid  | 添加额外高权限组 SID（权限提升）      | S-1-5-21-...-512,S-1-5-21-...-519       | 跨森林或提权              |
| -extra-pac  | 添加 UPN_DNS_INFO（补丁兼容性增强）   | 无值（开关）                            | 新补丁环境保险            |
| -spn        | 服务 SPN（Silver Ticket 必填）        | cifs/dc.administrator.htb               | Silver Ticket 生成        |



## Golden Ticket（黄金票据）

### 1）介绍

伪造对象：TGT

签名密钥：krbtgt的NTLM hash/AES key

权限级别：域管理员（甚至域本身）

特点：

（1）可以访问任何服务

（2）可以任意指定用户、SID、组

（3）域内永不过期（直到krgtbt重置）

### 2）材料来源（krbtgt NTLM Hash）

（1）secretsdump.py(DCSync)

（2）DC上的ntds.nt

（3）本地的LSASS dump（极少）

没有DCSync=基本造不了Gloden Ticket

### 3）用法

```
#生成TGT证书
impacket-ticketer -nthash aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  -domain-sid S-1-5-21-111111111-222222222-333333333 -domain administrator.htb administrator
#使用TGT证书
export KRB5CCNAME=administrator.ccache
klist
smbclient.py -k -no-pass administrator.htb@dc.administrator.htb
```



## Silver Ticket（白银票据）

### 1）介绍

伪造对象：TGS

签名密钥：服务账号的NTLM hash

特点：

（1）只对某以主机+某一服务有效

（2）不经过DC（日志少）

（3）权限范围更小，但更隐蔽

### 2）材料来源（服务账号 NTLM Hash）

（1）机器账号（HOSTNAME$)

（2）SQL服务账号

（3）IIS AppPool账号

（4）gMSA账号

非DA权限也可能做到

### 3）SPN服务名称

| 服务  | SPN                 |
| ----- | ------------------- |
| SMB   | cifs/hostname       |
| WimRM | http/hostname       |
| MSSQL | mssql/hostname:port |
| LDAP  | ldap/hostname       |
| HOST  | host/hostname       |

### 4）用法

```
#生成TGS证书
impacket-ticketer -nthash <SERVICE_COMPUTER_HASH> -domain-sid <SID> -domain administrator.htb -spn cifs/dc.administrator.htb administrator
#使用TGS证书
export KRB5CCNAME=administrator.ccache
klist
smbclient.py -k -no-pass administrator.htb@dc.administrator.htb
```

## Golden Ticket防守视角

### 1）Golden Ticket检测难点

（1）票据本身是否“合法签名”

只能靠

（1）异常SID

（2）异常有效期

（3）krbtgt轮换

### 2）防守要点

（1）定期重置krbtgt（2次）

（2）限制DCSync权限

（3）监控异常的Kerberos生命周期

## 注意事项

（1）版本问题：旧版 Impacket 在 patched 环境（KB5008380 补丁后）生成的票据会被撤销（KDC_ERR_TGT_REVOKED）。建议用最新 GitHub master 分支，或备选 Rubeus.exe。

（2）时钟同步：Kerberos 对时间敏感，执行前 ntpdate DC_IP 同步时间。

（3）OPSEC：Golden Ticket 日志少，但寿命过长易被检测；Silver Ticket 更隐蔽。

（4）报告写作：考试报告中详细描述 “利用 krbtgt NTLM 哈希通过 ticketer.py 伪造 Golden Ticket，实现域持久化”。