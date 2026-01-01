# Swaks

## 介绍

Swaks（Swiss Army Knife for SMTP)是一款非常实用的SMTP测试工具，用来调试、测试邮件服务器、验证邮件发送流程。它的特点强大、灵活、易用，常用来排查邮件投递问题。

## 参数

### 1）目标与基本参数

| 参数            | 说明             |
| --------------- | ---------------- |
| --to <addr>     | 收件人           |
| --from <addr>   | 发件人           |
| --server <host> | smtp服务器地址   |
| --port <port>   | 默认是25         |
| --helo <name>   | 自定义 helo/ehlo |

#### 2）认证相关（SMTP AUTH）

| 参数                   | 说明                               |
| ---------------------- | ---------------------------------- |
| --auth                 | 启用认证                           |
| --auth-user <user>     | 认证用户名                         |
| --auth-password <pass> | 认证密码                           |
| --auth-type <type>     | 指定认证方式(LOGIN/PLAIN/CRAM-MD5) |

### 3）TLS/SSL加密

| 参数             | 说明                   |
| ---------------- | ---------------------- |
| --tls            | 使用STARTTLS           |
| --tls-on-connect | 连接即TLS（常用于465） |
| --tls-optional   | TLS可选（失败不终止）  |
| --tls-verify     | 校验证书               |
| --tls-no-verify  | 不校验证书             |

### 4）邮件内容控制

| 参数                  | 说明           |
| --------------------- | -------------- |
| --data <string>       | 自定义邮件正文 |
| --body <string>       | 仅正文         |
| --header "key: Value" | 添加自定义头   |
| --attach <file>       | 添加附件       |
| --ehlo <name>         | 指定EHLO名称   |

### 5）调试报错

| 参数                | 说明           |
| ------------------- | -------------- |
| -v / --verbose      | 详细输出       |
| --debug             | 更详细输出     |
| --quit-after <step> | 在指定阶段退出 |
| --timeout <sec>     | 超时时间       |

### 6）连接控制/行为模式

| 参数                    | 说明                |
| ----------------------- | ------------------- |
| --protocol SMTP         | 指定协议            |
| --local-hostname <name> | 指定本机主机名      |
| --pipeline              | 使用SMTP PIPELINING |
| --force                 | 忽略错误继续        |

## 常见用法

### 1）发送最简单的测试邮件

swaks --to test@example.com --server smtp.example.com

### 2）使用SMTP AUTH发送邮件

swaks --to test@example.com --from me@example.com --server smtp.example.com --auth --auth-user me@eaxmple.com --auth-password 'youpassword'

### 3）使用TLS

swaks --to test@example.com --server smtp.example.com --tls

### 4）查看Raw SMTP 交互

它默认就会打印客户端与服务器之间的完整对话

## swaks能做什么？

（1）发送测试邮件（支持普通SMTP、SSL、TLS）

（2）测试SMTP认证（LOGIN/PLAIN/CRAM-MD5等）

（3）查看邮件服务器返回的完整交互日志

（4）模拟各种邮件场景（自定义头、邮件、附件等）

（5）可以用来判断代码问题？还是SMTP服务端拒信？还是认证失败？

## 25、465、587端口区别

### 1）25端口（老版本）

特点：（1）SMTP最早的标准接口（2）默认明文（3）用于邮件服务器之间转发 （4）很多厂商已经默认封掉

### 2）465端口（一上来就加密）

特点：（1）连接建立就走SSL/TLS （2）全程加密 （3）通常必须AUTH （4）现在被重新定义标准（SMTPS）

### 3）587端口（推荐）

特点：（1）先明文连接再STARTTLS （2）标准的邮件提交端口 （3）必须AUTH （4）云邮箱默认