# TGT和TGS

## TGT（Ticket Granting Ticket）

###  作用

向域控(KDC)申请其他服务的票

### 本质

我是某个用户，这是DC给我背书的身份证

## TGS（Ticket Granting Service）

### 作用

1）访问某个具体服务

### 绑定：

1）SPN+服务账号

2）只能给那个服务使用



## LSASS里的票据能不能“拿到别的机器上用”

### 1）TGT:可用跨机器使用（在条件满足时）

从LSASS拿到某用户有效TGT

1）可用在另一个机器上用

2）把这张TGT放进一个会话

3）再去向DC申请新的TGS

这等价于我就是这个用户

### 2）TGS:通常不能随便跨机器使用

1）绑定服务SPN

2）绑定加密密钥（服务账号）

所以拿到cifs/serverA不能b访问cifs/serverB

## 为什么TGS也能横向

拿到cits/serverA的TGS

访问serverA的文件共享

但是不能用它访问别的服务

不能用它去换别的服务

## 使用这些票据硬性限制条件

1）票据还没过期

TGT/TGS都有有效期

过期=作废

2）域SID/Realm匹配

票据属于那个域

只能在那个域里用

3）放进正确的安全上下文

票据必须被加载进Kerberos会话

系统才会那他做认证
	4）服务端是否开启Kerberos

有些服务只用NTLM

那么TGS就用不上用场

## TGT有权限信息吗？

TGT/TGS不直接存权限，只存身份信息，权限是目标系统决定的。

Kerberos只负责告诉“你是谁？”

Windows本地系统负责“你能干什么？”

### 权限相关

1.域身份/组成员(Domain Admin、Domain Users)

2.本地权限(是否本机管理员)

3.系统特权(SeImpersonate、SeDebug)

TGT/TGS只和第一个身份信息有关

### TGT里有什么

用户的SID

用户的域SID

用户的PAC(Privilege Attribute Certificate)

时间戳、有效期

会话密钥

### PAC是不是权限？

PAC=用户域层面的身份属性

PAC里包含：

1）用户SID

2）用户所属的域组SID

​	Domain Users、Domain Admins、Enterprise Admins

3）其他域级属性

## TGS有权限信息吗？

TGS的作用向某个服务证明我是谁？

TGS包含：

1）同样的PAC

2）针对某个SPN的服务票据

3）服务会话密钥

## 权限在哪里决定的？

### 1）Kerberos阶段(TGT/TGS)

确认身份+域组成员

输出结果

这个人是张三

它是Domain Admins/Domain Users

### 2）目标主机本地（登录/访问时）

Windows会

1.读取票据里的PAC

2.生成Access Token

3.把

1）用户SID

2）域组SID

4.本地组、本地策略合并

5.得到最终Token

## 为什么同一个域管理员、在不同机器权限不同？

因为：

1）PAC一样（域身份一样）

2）本地组、本地策略不同

机器A：Domain Admin > 本地Administrators

机器B：Domain Admin 被移除

## TGT、TGS、Token、ACL

TGT/TGS->身份(域级)

Access Token->本地可执行权限

ACL->对具体对象的访问规则

## 总结

Kerberos票据不给权限，只携带身份，权限由目标系统根据身份生成Token决定。