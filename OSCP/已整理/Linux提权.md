## Linux提权

#### 身份

whoami

id

pwd

hostname

uname -a

echo $PATH



#### 能做什么

sudo -l

查看配置NOPASSWD的命令

tar

vim

nano

find

python、perl、php

less、moss、man



有那些SUID

find / -type f -perm -4000 2>/dev/null

重点看：不常见的自定义二进制

看nmap、vim、find、bash、python 被打suid

某些程序用了省略路径 用PATH劫持

查SGID

#### 定时任务

当前用户cron

crontab -l 2>/dev/null

全局cron

ls -al /etc/cron* 2>/dev/null

cat /etc/crontab 2 >/dev/null

看有没有以root身份定时运行的脚本

那些脚本、路径是否可写

ls -al /path/to/script.sh 

#### PATH劫持

1.看PATH echo $PATH

2.PATH里是否有普通用户可写目录

echo $PATH | tr ':' '\n' |ls -ld <dir>

#### 配置文件/备份/明文密码

重点目录：

Web目录

ls -al /var/www

ls -al /var/www/html

常见配置文件

grep -Ri "password" /var/www 2>/dev/null

grep -Ri "DB_PASS" /var/www 2>/dev/null

home目录下的脚本或备份

ls -al /home

ls -al /home/*/

find /home -maxdepth 3 -type f \(-name "*.bak"\) 2>/dev/null'

#### SSH、密钥、历史记录

SSH私钥

find /home -name "id_rsa" 2>/dev/null

find /root -name "id_rsa" 2>/dev/null

命令历史

cat ~/.bash_history 2>/dev/null

cat /home/*/.bash_history 2>/dev/null

网络&本地服务（横向+本地exploit）

监听端口

ss -tunlp 2>/dev/null || netstat -tunlp 2>/dev/null

只绑定127.0.0.1的服务

本地Redis/Mysql/Web服务

可以本机链接利用：mysql -u root、redis-cli等

内网其他端口（做pivot用）

#### 内核&漏洞(exploit提权)

内核版本

uname -a

发行版

cat /etc/issue

#### 特殊组/容器/特权能力(capablities)

cat /etc/group

id

看看有没有

docker

lxd

disk

sudo(规则限制)

有可能用

Docket escape

LXD容器提权

getcap -r / 2>/dev/null

#### 看用户目录和web目录

ls -al /home

ls -al /root 2>/dev/null

ls -al /var/www 2>/dev/null

网络情况

ss -tunlp 2>/dev/null || netstat -tunlp 2>/dev/null



#### 检查顺序

##### 1）上下文

###### 1.1确认权限

id;groups

###### 1.2 系统版本 内核版本

cat /etc/os-release 2>/dev/null;

uname -a;

###### 1.3 环境变量

env | head;echo$PATH

##### 2)sudo路线（优先级最高）

sudo -l 

NOPASSWD应用

##### 3）账号、凭证

WEB配置、备份、脚本

ls -al /var/www/  2>/dev/null

grep -Ri "password\\|passwd\\|secret\\|token\\|api_key\\|Authorization" /var/www 2>/dev/null | head -n 50

历史记录/SSH KEY

cat ~/.bash_history 2>/dev/null

find /home -maxdepth 3 -name "id_rsa" 2>/dev/null

##### 4）SUID,SGID 路线

find / -type f -perm -4000 2>/dev/null

find / -type f -perm -2000 2>/dev/null

重点看：不常见的应用，二进制文件，已经能执行修改和编辑的文件

##### 5）cron路线

crontab -l 2>/dev/null

cat /etc/crontab 2>/dev/null

ls -al /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly /etc/cron.d 2>/dev/null

对每个脚本看看 谁执行+我能不能写

ls -l /path/to/script

##### 6）可执行路径/文件（配置cron、服务、脚本）

find / -writable -type d 2>/dev/null | head

##### 7）PATH路径

echo $PATH | tr ':' '\\n'

ls -ld <dir>

##### 8）capaabilities

getcap -r / 2>/dev/null

##### 9）进程/服务/本地端口

ps aux --sort=-%cpu | head

ss -tunlp 2>/dev/null || netstat -tunlp 2>/dev/null

观察有没有只监听127.0.0.1的管理服务、数据库、内部web

##### 10）内核exploit

unma -a 、发行版本

sudo-凭证-suid-cron-cap-服务/进程-内核exploit

