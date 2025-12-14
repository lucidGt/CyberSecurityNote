# Jenkins

## 介绍

自动跑脚本、构建、部署代码的WEB服务（自带RCE能力的管理后台）

端口：8080

## 场景1：未授权访问

直接访问/、/manage、/script

没有登录要求，说明Jenkins没有锁

## 场景2：弱口令

admin：admin

jenkins：jenkins

通过别的密码复用

## 场景3：Script Console

Script Console

作用：1）管理员直接执行Groovy脚本、Groovy可以执行系统命令

## 场景4：Job/Build配置可控

新建Job、修改构建步骤、插入命令

## 思路

1）需要登录吗？2）有没有弱口令？ 3）能访问Script Console？ 4）能创建/修改Job吗？5）Jenkins运行用户是谁？

## 最小通过标准

看到Jenkins判断危险性

知道Script Console = RCE

知道登录可控Job = RCE

拿到Shell后Linux提权

