# ZIP-PasswordBruteforce

## zip2john

zip2john是John the Ripper工具的脚本,用于从ZIP提取密码哈希,便于后续破解.

## 流程

### 1)提取ZIP哈希

zip2john file.zip > hash.txt

### 2)运行john

john --wordlist=rockyou.txt hash.txt