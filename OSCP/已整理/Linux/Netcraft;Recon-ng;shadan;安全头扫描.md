## 被动信息收集

被动信息收集也称开源情报。OSINT



#### WEB侦察

##### 搜索引擎

site:<domain> <key>

fileType:<key>

##### WEB站点信息

社交媒体

WHOIS

whois <domain>

Registrant Name,Admin Name,Tech Name,Name Server,Email

##### 反向查询ip地址（地址所有者）

whois <ip>

#### Netcraft

英国互联网服务公司

DNS信息搜索信息 https://searchdns.netcraft.com/

子域，历史等信息

包含站点技术 site  technology

#### Recon-ng

模块化web信息收集框架，命令行工机

proxychains recon-ng

marketplace search github

K = Key

搜索安装模块信息

marketplace info 

marketplace install 

#### shodan网络空间搜索服务，发现服务器、设备、路由器、IOT等设备资产

net:<ip>/24

city:<key>

country:<key>



贴吧类服务http://pastebin.com

Stack Overflow https://stackoverflow.com

#### 安全头扫描器

Security Headers 分析HTPP相应头

常见头

Content-Security-Policy 基于白名单，防止游览器加载恶意资源（XSS）

X-Frame-Options 防止点击劫持

theHarvester -d xx.com -b google



