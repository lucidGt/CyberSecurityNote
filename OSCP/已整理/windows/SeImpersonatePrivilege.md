# SeImpersonatePrivilege

## 原理

SeImpresonatePrivilege允许持有者模拟（impersonate）客户端令牌。工具诱导SYSTEM级服务（如DCOM、Print Spooler、RPCSS）进行NTLM认证，捕捉SYSTEM令牌，然后用CreateProcessWithTokenW/AsUser执行任意命令提权至SYSTEM。

## JuicyPotato

### 支持版本

Windows 7/8/10 (至1803)/Server 2008-2016

### 流程

1. 启动恶意COM/RPC服务器监听端口。
2. 使用CoGetInstanceFromIStorage触发指定CLSID的DCOM对象激活（CLSID对应SYSTEM运行的COM服务器）。
3. DCOM激活时，RPCSS服务向恶意OXID Resolver认证（NTLM）。
4. 捕获SYSTEM NTLM认证，使用RpcImpersonateClient模拟SYSTEM令牌。
5. 用CreateProcessWithTokenW/CreateProcessAsUser以SYSTEM权限执行任意命令。

### JuicyPotato 常见有效 CLSID（按系统）：

- 默认（多数旧系统）：{4991d34b-80a1-4291-83b6-3328366b9097} (BITS)
- Windows 7/Server 2008：{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}, {6d18ad12-bde3-4393-b311-099c346e6df9}
- Windows 10/Server 2016：{4991d34b-80a1-4291-83b6-3328366b9097} 常有效

### 利用

JuicyPotato.exe -l <port> -p <cmd.exe> -t * -c <CLSID>

## PrintSpoofer

### 支持版本

Windows 10/Server 2016-2019 (需Print Spooler服务运行)

### 原理

利用Print Spooler服务（spoolsv.exe，SYSTEM权限）暴露的named pipe \pipe\spoolss。

1. 服务账户连接该pipe。
2. 使用RpcImpersonateClient模拟pipe另一端的客户端（实际为SYSTEM上下文的spoolsv）。
3. 捕获SYSTEM令牌。
4. 用CreateProcessWithTokenW/AsUser以SYSTEM权限执行命令。

### 要求

Print Spooler服务运行且可访问pipe。

### 利用

PrintSpoofer.exe -c "<command>" (-i 交互)

## RoguePotato

### 支持版本

Windows 10 build 1809+/Server 2019+

### 原理

1. 伪造OXID Resolver服务，注册恶意RPC接口。
2. 诱导SYSTEM级DCOM/RPCSS向伪造Resolver查询OXID。
3. 重定向认证至攻击者控制的named pipe。
4. SYSTEM上下文连接pipe，进行NTLM认证。
5. 使用SeImpersonatePrivilege调用RpcImpersonateClient捕获SYSTEM令牌。
6. 以SYSTEM权限执行命令。

### 利用

### 1）攻击机

sudo socat tcp-listen:135,reuseaddr,frok tcp:<target_ip>:9999

### 2）靶机

RoguePotato.exe -r <attacker_ip> -e "<command>" -l 9999 

## GodPotato

### 支持版本

Windows 8-11/Server 2012-2022 

### 原理

1. 启动本地RPC服务器，注册自定义接口。
2. 通过COM激活特定DCOM对象（SYSTEM上下文），操纵其OXID指向恶意服务器。
3. Hook RPCSS服务的dispatch table，拦截OXID解析过程。
4. 当SYSTEM上下文的RPCSS连接恶意接口时，触发NTLM认证。
5. 使用SeImpersonatePrivilege调用RpcImpersonateClient捕获SYSTEM令牌。
6. 以SYSTEM权限执行命令。

优势：绕过旧版限制，兼容Win8-11/Server2012-2022。

### 利用

GodPotato.exe -cmd ""