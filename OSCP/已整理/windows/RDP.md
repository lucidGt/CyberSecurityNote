# RDP（Remote Desktop Protocol）

收集：Windows账号，密码，允不允许RDP登录

## 场景1：登录

#### 来源：

Web配置文件、FTP、SMB泄露、数据库、密码复用

xfreerdp /u:username /p:password /v:target_ip

#### 实现：

完整windows桌面，cmd、powershell、windows本地提权

## 场景2：域环境中的RDP

普通域用户可能能RDP登录某些机器

登录后：

1.枚举本地管理员

2.抓更多凭据

3.横向移动

## 场景3：RDP登录后直接是管理员

用户在administrators组

RDP登录后

whoami /groups

直接拿最高权限

## 常用RDP工具

### xfreerdp

/u:user 用户名

/p:pass 密码

/v:targetIp IP

/d:CORP AD域名 等价与 /u:corp\\\user

/cert:ignore 忽略证书错误

/dynamic-resolution 自动分辨率

/clipboard 剪切板共享

/drive:share,/home/kali 映射本地目录到远程

/size:1280x800 固定粉白嫩绿

/sound:sys:alsa 声音

##### 普通登录

xfreerdp /u:user /p:pass /v:ip

##### 指定域

xfreerdp /u:domain\\\user /p:pass /v:ip

##### 常用参数

xfreerdp /u:user /p:pass /v:ip /cert:ignore /dynamic-resolution /clipboard

## 