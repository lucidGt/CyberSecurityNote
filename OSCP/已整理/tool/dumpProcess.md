# Dump

## Windows

（1）Task Manager:右键进程->创建转储文件（.dmp）

（2）ProcDump（Sysinternals）：procdump -ma <pid> 或者 prodump.exe -ma <process_name>

（3）PowerShell：Get-Process <name> | % {procdump -ma $_.Id}

## Linux

（1）live:core <pid>

（2）offline:/proc/<pid>/mem + dd if=/proc/<pid>/mem of=dump.bin

（3）procdump、gdb、gcore、dump memory