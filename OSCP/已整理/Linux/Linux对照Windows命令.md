# Linux对照Windows命令

## 身份/当前组

| 目的      | Linux       | Windows        |
| --------- | ----------- | -------------- |
| 我是谁    | whoami      | whoami         |
| 详细身份  | id          | whoami /all    |
| 当前Shell | echo $SHELL | echo %COMSPEC% |

## 用户&组

| 目的           | Linux             | Windows                       |
| -------------- | ----------------- | ----------------------------- |
| 当前用户所属组 | groups            | whoami /groups                |
| 查看某用户组   | id user           | net user user                 |
| 查看所有用户   | cat /etc/passwd   | net user                      |
| 查看所有组     | cat /etc/groups   | net localgroup                |
| 查看某组成员   | getent group sudo | net localgroup Administrators |

## 管理员/root判断

| 判断点       | Linux     | Windows         |
| ------------ | --------- | --------------- |
| 是否最高权限 | id->Uid=0 | whoam->SYSTEM   |
| 是否管理员   | sudo -l   | net session     |
| 管理员能力   | sudo      | Administrator组 |

Linux看Sudo，Windwos看组+特权

## 权限/特权（最容易提权的地方）

| 能力       | Linux                                  | Windows             |
| ---------- | -------------------------------------- | ------------------- |
| sudo权限   | sudo -l                                | X（用组替代）       |
| 特权列表   | getcap -r /                            | whoami /priv        |
| SUID程序   | find / -type f -perm -4000 2>/dev/null | X                   |
| SYSTEM权限 | uid=0                                  | NT AUTHORITY\SYSTEM |

Windows提权关键

SeImpersonatePrivilege

SeAssignPrimaryToken

SeDebugPrivilege

## 文件/目录权限（控制权）

| 目的     | Linux            | Windows                   |
| -------- | ---------------- | ------------------------- |
| 看特权   | ls -l            | icacls file               |
| 所有者   | stat file        | icacls file               |
| 可写文件 | find / -writable | accesschk.exe -uws user * |

## 服务/后台任务

| 目的            | Linux            | Windows         |
| --------------- | ---------------- | --------------- |
| 查看服务        | ps aux           | tasklist        |
| 服务详情        | systemctl status | sc qc service   |
| 定时任务        | crontab -l       | schtasks /query |
| root/System执行 | cron             | 服务/计划程序   |

## 网络信息

| 目的 | Linux    | Windows       |
| ---- | -------- | ------------- |
| 网卡 | ip a     | ipconfig /all |
| 路由 | ip route | route print   |
| 端口 | ss -lntp | netstat -ano  |

## 系统信息

| 目的   | Linux               | Windows       |
| ------ | ------------------- | ------------- |
| OS版本 | cat /etc/os-release | systeminfo    |
| 内核   | uname -a            | systeminfo    |
| 补丁   | dpkg -l             | wmic qfe list |

## 日志/凭据线索

| 目的     | Linux             | Windows           |
| -------- | ----------------- | ----------------- |
| 登录日志 | /var/log/auth.log | 事件查看器        |
| 日志权限 | adm组             | Event Log Readers |
| 历史命令 | .bash_history     | doskey /history   |

## 最小命令清单

### Linux

id

groups

sudo -l

find -type f -perm -4000 2>/dev/null

uname -a

### Windows

whoami

whoami /groups

whoami /priv

systeminfo