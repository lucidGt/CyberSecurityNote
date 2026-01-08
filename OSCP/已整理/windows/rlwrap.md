# rlwrap

## 介绍

rlwrap是个给"没有行编辑能力的交互程序"外挂一层ReadLine的小工具,让你在终端里用上:

↑/↓ **历史命令**

←/→ **光标移动**

**Backspace** 正常删除

`Ctrl+R` **反向搜索历史**

更舒服的交互体验（尤其是各种 shell、解释器、nc 之类）

##  1)让nc/socat的交互更像正常终端

```
rlwrap nc -lvvp 1443
注意:rlwrap只是改善你本地监听端的输入体验,而不是给对面"升级真TTY"

更输入
rlwrap -cAr nc -lnvp 443
```

## 2)给各种REPL/交互式工具加历史和编辑

rlwrap mysql -u root -p pass

rlwrap sqlite3 db.sqlite

rlwrap smbclient //ip/share -U user

rlwrap ftp ip

## 常用参数

-a : 把历史记录保存得更智能

-H <file> :指定历史文件(方便持久化)

rlwrap -a -H ~/.rlwrap_history nc -lvvp 4444

## rlwrap vs 升级tty

rlwrap:只是改善你本地输入的行编辑和历史

TTY升级:(python -c 'import pty;pty.spawm("/bin/bash")'/stty raw -echo等):让远端shell更像真终端(支持ctrl+c/tab补全/交互程序更正常)

rlwrap监听+进来后再做tty升级