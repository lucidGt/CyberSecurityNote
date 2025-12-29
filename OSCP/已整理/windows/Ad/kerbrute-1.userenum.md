# kerbrute userenum

## 原理

kerbrute userenum是利用kerberos对“用户名是否存在”的不同错误响应。

利用Kerberos AS-REQ（认证第一步）

客户端 → KDC (DC)

AS-REQ：我想要用户 X 的 TGT

关键点：这一步不需要密码，只需要用户名。

## 为什么有些域“userenum 不好用”

1）开启了kerberos预认证强策略+模糊错误

​	（1）DC返回统一错误

​	（2）userenum成功率下降

2）Azure AD/AAD Conenct混合环境

​	（1）响应被代理/抽象

​	（2）行为不一致

3）非标准Kerberos实现