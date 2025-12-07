### masscan

为扫描整个互联网涉及，6分支扫描整个互联网，每秒发送1000万个包

masscan实现自定义的TCP/IP堆栈，需要Raw Socket（sudo）

sudo apt install masscan

sudo masscan -p80 ip/8



### SMB服务

#### 扫描NetBIOS服务

TCP139、UDP137,138

SMB(TCP 445)和NETBIOS是两个独立的协议

NetBios是一个独立的会话协议和服务，允许本地网络主机之间相互通信

现代SMB可以在没有NetBios的情况工作

NBT(NetBios over TCP)兼容早期系统，经常与SMB共同使用

#### 端口扫描

nmap -p139,445 -oG smb.txt x.x.x.x1-x2

#### NetBios枚举工具

sudo nbtscan -r xx.xx.xx.xx/24

-r 通过 UDP 137查询NetBiso名称服务

#### NMAP SMB脚本

ls -l /usr/share/nmap/script/smb*

nmap -v -p 139,445 --script=xxx 1.1.1.1

### NFS服务

SUN Mircosystem 开发的分布式文件系统协议

允许客户端访问网络上其他主机的存储，就像本地存储一样

通常用于Linux系统，不安全的协议

#### NFS工作过程

Portmapper和RPCBind 服务运行在TCP 111上

RPC进程启动时通知RPCBind，注册监听端口和RPC程序号

客户端通过特定程序号联系服务端RPCBind，RPCBind重定向正确端口（通常是2049）

#### 端口扫描

nmap -v -p 111 x.x.x.x1-x2

#### 挂载NFS

mkdir home

sudo mount -o nolock x.x.x.x:/home ~/home/

cd home/user1 && ls -lan

#### 注意

可能服务端上的账号UID不一样，要自己在本地主机新建一个用户分配服务上的UID，使得拥有修改文件的权限。

### SMTP

邮箱服务器

