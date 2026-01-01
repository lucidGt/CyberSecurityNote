# lftp

## 介绍

lftp是一个“增强版FTP客户端”

支持：FTP/FTPS/SFTP/HTTP/HTTPS

比FTP稳、功能多、脚本友好。

## 连接方式

### 1）直接连接匿名

lftp ftp://anonymous:anonymous@10.129.5.106

### 2）指定用户名

lftp -u user,password ftp://10.129.5.106

## 文件传输

### 1）下载单个文件

get file.zip

### 2）下载并改名

get file.zip -o file2.zip

### 3）下载整个目录

mirror dir

### 4）上传文件

put file.zip

### 5）上传目录

mirror -R localdir

## 常用目录/查看命令

| 命令    | 作用         |
| ------- | ------------ |
| ls      | 列文件       |
| ls -la  | 详细列出     |
| cd dir  | 进入目录     |
| pwd     | 远端当前目录 |
| lpwd    | 本地当前目录 |
| lcd dir | 切换本地目录 |

## 注意

### 1）主动/被动模式

set ftp:passive-mode yes 被动模式（默认）

set ftp:passive-mode no 主动模式

### 2）二进制模式

默认开启 binary

### 3）断点续传

get -file.zip -c

## 脚本

默认进入主动模式

lftp -e 'set ftp:passive-mode no;' 'ftp://anonymous:anonymous@10.129.5.106'

## 卡在get/0字节

set ftp:passive-mode no

set ftp:use-epsv no

debug 3 #开调试模式