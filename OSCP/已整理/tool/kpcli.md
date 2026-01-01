# kpcli

## 介绍

kpcli是一个命令行KeePass(.kdbx)客户端，常用于Kali/linux快速、搜索、复制密码。

## 命令

| 命令           | 作用                                   |
| -------------- | -------------------------------------- |
| ls             | 列出当前组/条目                        |
| cd <组名>      | 进入某个组                             |
| cd ..          | 返回上一级                             |
| find <关键词>  | 全局搜索（标题/用户名/URL等）          |
| show -f <编号> | 显示某条目的详细字段（含用户名/URL等） |
| cp <编号>      | 复制密码到剪切板                       |
| edit <编号>    | 编辑条目                               |
| add            | 新增条目                               |
| save           | 保存到kdbx                             |
| close          | 关闭库                                 |
| quit           | 退出                                   |

## 场景

### 1）把数据库所有条目都搜一遍并显示

find .

### 2）find <pattern>

Title,Username,URL,Notes,组名(Group path)

