# gpp-decrypt

## 介绍

gpp-decrypt(Group Policy Preferences Decrypt,GPP密码解密工具)

### 漏洞背景

Windows Server 2008引入Group Policy Preferences(GPP),允许管理员通过组策略设置本地用户密码等,但密码以cpassword属性存储在SYSVOL共享的XML文件(如Group.xml)中,使用AES-256加密.

### 关键漏洞

微软使用的AES密钥是公开的(Microsoft Security Bulletin MS14-025承认),任何域用户都能读取SYSVOL文件,提取cpassword并解密得到明文密码(常用于本地管理员或服务账号).

## 用法

基本解密单个cpassword

```
gpp-decrypt 'j1Uyj3Vx8TY9LtLZil2uAuZkFQA/4latT76ZwgdHdhw'
输出明文密码（如 "Local*P4ssword!"）。
```

## 实战场景

(1)低权限用户访问SYSVOL共享(\\domain\\SYSVOL)

(2)搜索XML文件:find / -name Groups.xml 或者smbclient游览

(3)提取cpassword属性

(4)用gpp-decrypt解密->得到本地管理员密码->pth横向移动提权

## 自动化工具(平替)

(1)PowerView/Get-GPPPassword.ps1(powershell版)

(2)Metasploit post/windows/gather/credentials/gpp

(3)crackmapexec -M gpp_password