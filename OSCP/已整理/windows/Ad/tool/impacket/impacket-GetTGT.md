# impacket-GetTGT

## 介绍

impacket-GetTGT是用来“主动申请Kerberos TGT（票据）”的工具。

GetTGT=用“明文密码/NTLM/AES Key”，向KDC申请一个TGT，并保存成ccache文件。

流程

有凭据

   ↓

impacket-GetTGT

   ↓

拿到TGT(TGT.ccache)

   ↓

export KRB5CCNAME=xxx.ccache

   ↓

impacket-wmiexec/smbclient/getST/secretdump -k

## 常见用法

1）用明文密码拿TGT

impacket-GetTGT domain.local/user:password

2）使用TGT

export KRB5CCNAME=user.ccache

3）用NTLM hash（Pth->Kerberos）

impacket-GetTGT domain.local/user -hashes :NTHASH

​	(1)secretsdump / lsassy / mimikatz 拿到 hash

​	(2)但环境是 **Kerberos 优先**

4）用AES Key

impacket-GetTGT domain.local/user -aesKey <aes256_key>

​	（1）DCSync

​	（2）mimikatz `sekurlsa::ekeys`



## GetTGT 常见错误

（1）忘记了同步时间

sudo ntpdate dc.domain.local

否则出现：KRB_AP_ERR_SKEW

（2）SPN/主机名没配好

impacket-wmiexec -k -no-pass dc.domain.local