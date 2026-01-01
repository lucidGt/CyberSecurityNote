# kerbrute passwordspray

## 介绍

kerbrute passwordSpary 是Kerberos低频密码喷洒，是kerberos AS-REQ级别的认证尝试。

走AS-REQ协议，根据响应判断账号密码是否正确。

## 爆破跟喷洒策略区别

1）爆破

（1）1个用户

（2）N个密码

（3）很快锁定

2）喷洒

（1）N个用户

（2）1个密码

（3）低频、横向

## 利用工具

kerbrute passwordspray --dc 10.129.95.154 -d intelligence.htb users.txt 'Welcome123!'

- `users.txt`：你已经用 `userenum` 得到的真实用户名
- 密码：来自公司策略 / 季节 / 文件 / 默认口令

## 它为什么比 SMB spray 更“干净”

因为：

- 不走 SMB
- 不走 LDAP bind
- 不产生日志型登录失败（很多环境里）

## 8️⃣ OSCP 中最容易翻车的 3 个点（重点）

### ❌ 1. 对未枚举用户直接喷

→ 浪费请求 + 噪声 + 低成功率

### ❌ 2. 一次喷太多密码

→ 很容易触发锁定（考试直接 GG）

### ❌ 3. 对服务账号 / 机器账号乱喷

→ `$` 结尾账号通常不走这个逻辑