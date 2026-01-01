# firepwd

## 介绍

firepwd是把已保存登录的“加密结果”导出来，解密成功与否，取决于有没有主钥匙。

### 核心文件

| 文件       | 作用                |
| ---------- | ------------------- |
| login.json | 用户名+被加密的密码 |
| key4.db    | 加密/解密用的主密钥 |

## logins.json 里面有什么（结构层面）

你在靶机或自己机器看到的 json，通常长这样（简化）：

```
{
  "logins": [
    {
      "hostname": "https://example.com",
      "encryptedUsername": "MDoEEPgAAAAAAAAA...",
      "encryptedPassword": "MDoEEPgAAAAAAAAA...",
      "timeCreated": 1690000000000
    }
  ]
}
```

注意几个点（OSCP/实战常考）：

- `encryptedUsername`
- `encryptedPassword`

👉 都不是 hash

👉 是Firefox 用 NSS（Network Security Services）加密过的 blob

## 用途

1）完整用户画像

​	（1）登录过那些站点

​	（2）内网系统/Jenkins/GitLab/VPN Portal

2）配合key4.db

​	（1）在同一用户上下文下->可以被解密

3）取证

​	时间线：什么时候第一次登录某系统

4）是否值得深挖

​	看jekins,vpn等等关键词 判断高价值用户

## 命令

（1）把login.json，key4.db放到firepwd目录下

（2）python3 firepwd