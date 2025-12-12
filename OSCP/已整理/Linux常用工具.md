## Linux常用工具

### tar

-c = create 创建包

-v = verbose 显示过程

-f = fileName 指定输出文件名

-x = extract 解包

-z = gzip模式 (.gz/.tgz)

-C = 解压到指定目录

### python

#### 运行与交互

--version 版本号

-c 解析执行代码

-m module 以模块方式运行

#### pip包管理

-m pip --version 版本号

-m pip install 安装

-m pip install -U 升级

-m pip uninstall 卸载

-m pip list pip列表

-m pip show pack 显示包

#### 虚拟环境(venv) 每个项目一个

python -m venv .venv

##### 激活

###### linux

souce .venv/bin/activate

###### windows

.\\.venv\\Scripts\\Activate.ps1

###### 退出

deactivate

#### 常用模块 -m

python -m http.server 8000 静态服务器

python -m json.tool json格式化检验

python -m site  看site-packages等路径

python -m pip 用pip推荐方式

python -m venv .venv 建虚拟环境

#### 路径与环境排查

which python

where python

python -m pip -V

#### 依赖与项目常见工作流

python -m pip install -e 以可编辑的方式安装本项目

python -m pip install build 

python -m build 构建包

### Perl(通用脚本语言) (Practical Extraction and Reporting Language)

主要是老版本的exploit利用语言

好处是老版本的Linux：自带Perl，需要依赖少

变量$a、$b

system()/cmd

/xxx/

运行perl xx.pl



### Lees(分页查看器)

向下翻一页	Space

向上翻一页	b

向下滚一行	Enter

退出	q

搜索	/关键词

下一个匹配	n

上一个匹配	N

显示当前行号	=



#### 常用法

dmesg|less

ps aux | less

less -N exploit.c

man less



### php

1)Sql注入

原因：拼接SQL字符串、未用参数化查询

修复：PDO/MYSQLI预处理

函数：query(),mysqli_query(),$\_GET,$\_POS



2）命令注入

原因：exec/system/sheel_exec_passthru带入shell

修复：尽量不用shell，白名单参数

函数：exec()、shell_exec()、system()

2.1 exec

$output = [];

$code = 0;

$lastLine = exec("whoami",$output,$code);

2.2 shell_exec()

$all = shell_exec("ls -la");

2.3 system()

$code = 0;

$LastLine = system("data",$code);



3）文件上传漏洞（webShell/任意文件写入）

原因：只靠拓展名判断、上传目录可执行、没做真实MIME检查

修复：

上传目录设置为不可执行

文件名重写（随机）

白名单文件类型（图片）+校验内容

限制大小、数量、频率

函数：move_uploaded_file

3.1 move_uploaded_file

move_uploaded_file($tmp,$dest);



4）本地/远程包含（LFI/RFI）

原因：include/require 动态拼路径，路径来源客户端

修复：只做固定映射训责；realpath限制在目录内

函数：include($_GET、require($path)



5）目录遍历（Path Traversal）

原因：下载/读取文件接口用客户端上的数据

修复：白名单；前缀检查；禁止特殊符号



6)XSS（跨站脚本）

原因：把用户内容原样输出到HTML/JS/属性里

修复：输出安上下文转义；模板引擎默认转义；设置CSP

1.设置httpOly

​	php.ini

​	seesion.cookie_httponly=1

​	setcookie(

​	...,

​	[

"httponly"=>true,针对JavaScript偷Xss

"secure"=>true,针对抓包分析

"samesite"=>"Lax"防跨站申请 CSRF

]

);





函数：echo $Get $Port 数据内容 输出





7)CSRF（Cross-Site Request Forgery)

原因：改密码、转账、绑定邮箱 没有CSRF Token

修复：表单请求加CSRF；Cookie Check；对敏感操作加二次验证=



8）认证/会话问题

风险：弱口令，验证码绕过，seesion固定，cookie没http only/secure/samesize

修复：登录限速、强密码策略、2FA；设置正确COOKIE





9）反序列化漏洞（PHP Object Inject）

原因：unserialize()处理不可信输入

修复：不要反序列化用户输出；改用json；限制allowd_classes

函数：unserialize()



10）信息泄露/配置错误

原因：display_errors=On，泄露.env、暴露phpinfo、debug页面

修复：关闭debug模式；限制敏感文件访问；关闭提示

### netstat

-t 只看TCP

-u 只看UDP

-l 只看正在监听

-n 用数字显示（不把端口解析成服务名、不把IP反查域名）

-p 显示进程ID

Recv-Q/Send-Q：接收和发送队列等待处理的数据量

LocalAccess：本地监听地址：端口

Foreigin Address：对端地址

State（TCP才有）：LISTEN表示正在连接：UDP一般没有状态

### getcap -r / 2>/dev/null

高风险

cap_setuid：可能直接变成Root

cap_setgid：可能拿到高权限组

cap_dac_override：绕过大多数文件的权限检查

cap_dac_read_search：绕过读权限/目录遍历

cap_fowner：可改不属于自己文件的权限

cap_chown：可改属主

cap_sys_admin：root

cap_sys_ptrace：可ptrace其他进程，可能读内存/偷凭证

cap_sys_module：可加载内核模块

中风险

cap_net_admin：能做网络管理/抓包

cap_net_raw：能发raw包

cap_net_bind_service：绑定1024以下端口

低风险

cap_sys_nice：调整优先级/调度
