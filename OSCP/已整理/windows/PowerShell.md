# PowerShell

## 介绍

PowerShell是一个“以对象为核心的”自动化Shell和脚本语言。

Shell+脚本+对象

## Linux/CMD和PowerShell对比

### Linux/CMD

```
命令->文本->文本->文本
```

（1）ls | grep | wak

（2）管道流的字符串

（3）你要解析空格、列、格式

### PowerShell

```
命令->对象->对象->对象
```

(1)管道里里的是结构化对象

(2)每个对象都有:属性+方法

(3)不用"猜格式"

这就是PowerShell的核心思想

## Powershell的三大设计思想

(1)一切皆是[对象],不是文本

Get-Process输出的不是PID,Name,CPU

而是System.Diagnostics.Process

你可以直接 Get-Process | Select-Object Name,Id,CPU

(2)管道传的是[对象],不是字符串

Linux管道

ps aux | grep root

Powershell管道

Get-Process | Where-Object CPU -gt 100

左边输出的是Process对象,右边直接用.CPU这个属性

管道=对象流水线

(3)统一抽象:Provider思想

PowerShell把很多系统自由,伪装成目录树

| 看起来像   | 实际是   |
| ---------- | -------- |
| C:\        | 文件系统 |
| HKLM:\     | 注册表   |
| Cert:\     | 证书     |
| Env:\      | 环境变量 |
| Variable:\ | 变量     |

所以可以用同一套命令:

Get-ChildItem

去列:

​	(1)文件

​	(2)注册表键

​	(3)证书

​	(4)变量

## PowerShell自动变量(Automatic Variables)

### 路径与位置类

| 参数           | 作用               |
| -------------- | ------------------ |
| $pwd           | 当前目录           |
| $home          | 当前用户的主目录   |
| $PSScriptRoot  | 脚本所在目录       |
| $PSCommandPath | 当前脚本的完整路径 |

小技巧:$pwd是对象,$pwd.Path才是字符串路径

### 上一条命令状态类

| 参数          | 作用                                 |
| ------------- | ------------------------------------ |
| $?            | 上一条命令是否成功                   |
| $LASTEXITCODE | 上一条外部程序(exe)退出码(0代表成功) |
| $Error        | 错误记录数组                         |

### 管道与当前对象类

| 参数   | 作用                                                   |
| ------ | ------------------------------------------------------ |
| $_     | 管道里的"当前对象" (ForEach-Object / Where-Object常用) |
| $args  | 传给脚本/函数的位置参数数组                            |
| $input | 管道输入集合                                           |

### 进程与环境类

| 参数            | 作用                                               |
| --------------- | -------------------------------------------------- |
| $PID            | 当前PowerShell进程Id                               |
| $PSVersionTable | PowerShell版本信息                                 |
| $env:Name       | 环境变量($env:USERPROFILE / $env:PATH / $env:TEMP) |

### 其他常用

| 参数         | 作用       |
| ------------ | ---------- |
| $null        | 空值       |
| $true/$false | 布尔值     |
| $PSItem:     | 基本等价$_ |

Get-Variable

Get-ChildItem

## PowerShell的命令哲学

(1)动词-名词(Vedr-Noun)

Get-ChildItem

Set-ExecutionPolicy

Remove-Item

Select-Object

目前只有一个:可读,可发现,可补全

Get-Command Get-*

Get-Command *-Process

(2)命令!=程序

| 类型         | 例子          |
| ------------ | ------------- |
| Cmdlet(原生) | Get-ChildItem |
| Alias(别名)  | gci,ls        |
| 外部程序     | ping,nmap     |

PowerShell是调度者,不是指能跑自己命令的shell.

## PowerShell的标准三件套思想

| 语法          | 作用     |
| ------------- | -------- |
| Get-xxx       | 拿对象   |
| Where-Object  | 过滤对象 |
| Select-Object | 整理对象 |

找出所有文件->过滤大文件->列成表

## Where-Object

### 作用:根据条件,决定"要不要这个对象"

接收的对象:

​	(1)文件(FileInfo)

​	(2)进程(Process)

​	(3)AD对象

​	(4)Select-String的MatchInfo

### 参数

| 语法                                           | 含义           |
| ---------------------------------------------- | -------------- |
| $_                                             | 当前管道对象   |
| -eq (Equal)                                    | 等于           |
| -ne (Not Equal)                                | 不等于         |
| -gt (Greater Than)                             | 大于           |
| -ge (Greater Than or Equal)                    | 大于等于       |
| -lt (Less Than)                                | 小于           |
| -le (Less Than or Equal)                       | 小于等于       |
| -like                                          | 通匹配符匹配   |
| -notlike                                       | 通匹配符不匹配 |
| -match                                         | 正则匹配       |
| -notmatch                                      | 正则不匹配     |
| -contains(默认就是-icontains),默认不区分大小写 | 包含(集合)     |
| -ccontains (case-sensitive)                    | 区分大小写版   |
| -icontains (ignore-case)                       | 不区分大小写   |

### 1)脚本块模式

Get-ChildItem | Where-Object {$_.length -gt 1MB}

### 2)简易参数模式

Get-Process | Where-Object CPU -gt 100

Get-childItem | Where-Object Name -Like "*.ini"

### 3)什么时候用WhereObject?

(1)条件判断 (2)帅选不要的对象 (3)相当于if + filter

### 4)contains用法

$groups = @("Admin","HR","IT")

$groups -contains "Admin" #True

$groups -contains "Sales" #False 

## Select-Object - (选字段/改形状/去重/截断)

| 参数            | 作用         |
| --------------- | ------------ |
| 属性名          | 选字段       |
| -ExpandProperty | 只输出属性值 |
| -Fisrt n        | 取前n个      |
| -Last n         | 取后n个      |
| -Unique         | 去重         |
| @{}             | 计算字段     |
| -Property       | 显示指定属性 |

### 作用:不决定"要不要",只决定"输出长什么样子"

接收的对象

​	(1)任何对象

### 1)选属性(最基本)

Select-object Name,FullName

### 2) -ExpandProperty (非常重要)

select-object -ExpandProperty Fullname

| 行为       | 结果                              |
| ---------- | --------------------------------- |
| 不用Expand | 输出对象本身                      |
| 用Expand   | 输出对象的属性值本身(字符串/数组) |

做导出/传给外部程序用

### 3) -First/-Last

Select-Object -First 10

Select-Object -Last 10

截断对象流(性能优化用)

### 4) -Unique

Select-Object Externsion -Unique

去重(基于属性值)

### 5) -自定义列(计算字段)

Select-Object Name,@{Name="sizeMbB;Expression={[math]::Round($_.Length/1MB,2)}}

### 6) -Property (等价写法)

Select-Object -Property Name,Length

## Select-String - [搜内容/grep]

### 作用:在"文本内容"里搜索关键词或正则

接收对象:(1)字符串 (2)文本对象(FileInfo)

### 1)参数

| 参数           | 含义                   |
| -------------- | ---------------------- |
| -Pattern       | 普通字符串,正则表达式  |
| -CaseSensitive | 是否区分大小写         |
| -SimpleMatch   | 不当正则,纯字符串匹配  |
| -Path          | 不用管道,直接搜文件    |
| -Include       | 包含文件               |
| -Exclude       | 不包含文件             |
| -Context       | 显示前后行(grep -C)    |
| -AllMatches    | 一行多个匹配全部抓出来 |

### 2)输出对象

| 属性       | 含义         |
| ---------- | ------------ |
| Path       | 文本路径     |
| LineNumber | 行号         |
| Line       | 命中内容     |
| Matches    | 正则匹配结果 |

### 3) -Pattern(必须)

Select-String -Pattern "password"

### 4) -CaseSensitive

-CaseSensitive:$true

-CaseSensitive:$false

是否区分大小写

### 5) -SimpleMatch

-SimpleMatch

不当正则,纯字符串匹配

### 6) -Path

Select-String -Path *.ini -Pattern "password"

不用管道,直接搜文件

### 7) -Include / -Exclude

-Include *.ini

-Exclude *.log

过滤文件

### 8) -Context

-Context 2,2

显示前后行 (grep -C)

### 9) -AllMatches

-AllMatches

一行多个匹配结果抓出来

## 特殊用法

Get-Item -Path $pwd -Stream * -Force 查看隐藏文件，包括文件流

Get-Item -Path .\\\* -Stream * -Force 查看隐藏文件，包括文件流

## PowerShell Vs Bash

| Bash     | PowerShell   |
| -------- | ------------ |
| 文本管道 | 对象管道     |
| 快\短\小 | 稳\强\结构化 |
| 适合Unix | 适合Windows  |

不是谁取代谁,设计目标不同.