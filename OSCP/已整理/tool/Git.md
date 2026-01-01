# Git

## 介绍

Git分布式版本控制

## 价值

1）历史源码

2）被删掉的密码/key/token

3）配置文件（数据库、api、ssh）

4）开发者习惯

## 场景1：Web目录暴露了.git/

/.git/或/.git/config

## 场景2：已经拿到服务器Shell

ls -a 

.git/

说明这个Web程序目录是Git仓库

## 利用方式

1）拉取仓库代码审查

2）log日志

3）commit注释

4）分支/环境配置

## 操作

### 快速了解仓库状态

git status

git brach -a

git remote -v

git rev-parse --is-inside-work-tree

### 更好用的日志

git log --online --decorate --graph --all

git log -p #每次提交的Diff

git log --name-only #每次提交涉及那些文件

git log --stat #你已经会了

git log -- <path/to/file> #只看某个文件的历史

### 看文件在某个提交时的内容（不用切分支）

git show<hash>:path/to/file

git show <hash>:config.php

### 找被删掉被重命名的文件

git log --diff-filter=D --summary #找删除

git log --diff-filter=R --summary #找重命名

git log --all --path/to/file #找文件去哪里了

### 在提交历史里搜敏感信息

在当前工作区搜索：

git grep -n "password\\|passwd\\|secret\\|token\\|api_key\\|key"

在全部历史搜索：

git log -S "password" --online --all

git log -G "password|token|secret" --online --all

-S:查某个字符串出现、消失的提交

-G:用正则查diff

### 恢复文件/撤销操作

从某个提交把文件恢复到当前分支

git checkout <hash> -- path/to/file

撤销本地改动

git restore path/to/file

git checkout -- path/to/file

回到最新状态

git switch main

git checkout master

### 对比差异

对比最新提交

git diff

对比两个提交

git diff <hash1> <hash2>

对比两个分支

git diff main..dev

### 查看提交历史

git log

### 看某次提交改了说明

git show <commit_hash>

### 看被删掉的文件

git log --stat

### 恢复某次提交的内容

git checkout <commit_hash>

## 最小通过标准

知道.git暴露很危险

会看commit历史

会找被删掉的敏感信息

会把Git线索接到web/ssh/db