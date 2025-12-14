# SMTP(Simple Mail Transfer Protocol)

端口：25常见 587提交端口 465(SMTPS)

价值：用户枚举+信息收集

能不能枚举用户名

拿到邮箱地址格式

能不能为SSH、SMB、RDP、Winrm提供用户列表

## 场景1：用户名枚举

SMTP支持命令

VRFY() = Verify 验证用户

EXPN() = Expand 展开列表

RCPT TO = Recipient 指定收件人

用来判断用户是否存在

## 场景2：收集邮箱、域信息

SMTP banner和响应里经常泄露

主机名、域名、邮箱地址格式

## 场景3：邮件内容线索

临时密码、重置链接、内部系统地址

## 常用工具

#### smtp-user-enum

smtp-user-enum -M VRFY -U user.txt -t target_ip

### nmap smtp脚本

nmap -p25 --script smtp-enum-users target_ip

### nc（手动测试）

nc target_ip 25