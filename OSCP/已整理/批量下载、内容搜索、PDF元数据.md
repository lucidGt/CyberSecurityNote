## 批量下载

批量下载断点续传

wget -i urls.txt -P downloads/ -c

## 文件内容搜索

忽略大小写搜索显示文件名

grep -Rin "admin" .

对所有文件字符串搜索

strings * | grep -i 'password'

## PDF内容搜索

对目录下所有PDF内容搜索

pdfgrep -rin 'password'

#或者

pdftotext file.pdf - | grep -i 'password'

## PDF元数据枚举

### exiftool (Exchangeable Image File Format)

批量查看DPF元数据

exiftool *.pdf

递归整个目录

exiftool -r .