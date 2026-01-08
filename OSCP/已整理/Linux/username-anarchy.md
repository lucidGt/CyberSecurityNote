# username-anarchy

## 介绍

username-anaychy用于从真实名字(firstname lastname)生成常见的用户名变体列表.

## 参数

#### **参数表格**

| 参数（短/长）            | 描述                                                         | 示例/说明                                     |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------- |
| -i, --input-file FILE    | 输入姓名列表文件（支持SPACE、CSV、TAB分隔）。默认列：firstname, lastname。支持列头：firstinitial, firstname 等。 | username-anarchy -i names.txt                 |
| -a, --auto               | 自动生成姓名（结合--country使用）。                          | username-anarchy -a --country china           |
| -c, --country COUNTRY    | 指定国家数据集生成常见姓名（PublicProfiler国家或Facebook top 10000）。 | COUNTRY: argentina, austria, china, france 等 |
| --given-names FILE       | 自定义given names字典文件。                                  | 指定常见名文件                                |
| --family-names FILE      | 自定义family names字典文件。                                 | 指定常见姓文件                                |
| -s, --substitute STATE   | 控制姓名替换（on/off）。默认off（替换缺失部分，如initial + last）。 | -s on                                         |
| -m, --max-sub NUM        | 每插件替换数量限制。默认-1（无限）。                         | -m 10                                         |
| -l, --list-formats       | 列出所有格式插件（first.last, flast 等）。                   | username-anarchy -l                           |
| -f, --select-format LIST | 选择特定插件（逗号分隔）。                                   | --select-format first.last,flast              |
| -r, --recognise USERNAME | 识别用户名格式（用Facebook数据集）。                         | --recognise j.smith                           |
| -F, --format FORMAT      | 自定义格式（format string或ABK格式）。                       | -F "%f.%l" 或 -F "v-annakey"                  |
| -@, --suffix SUFFIX      | 添加后缀（如@email.com）。                                   | --suffix @example.com                         |
| -C, --case-insensitive   | 大小写不敏感（默认True，全小写）。                           | 默认全小写                                    |
| -v, --verbose            | 详细输出（显示插件注释和搜索进度）。                         | -v                                            |
| -h, --help               | 显示帮助信息。                                               | username-anarchy -h                           |

| 插件名称       | 生成格式示例（Anna Key） | 解释（常见企业规则）                    | OSCP应用场景                      |
| -------------- | ------------------------ | --------------------------------------- | --------------------------------- |
| **first.last** | anna.key                 | firstname.lastname（点分隔，全小写）    | 最常见（如Microsoft、Google风格） |
| **flast**      | akey                     | first initial + lastname（首字母+姓）   | 短用户名（如Unix旧系统）          |
| **firstl**     | annak                    | firstname + last initial（名+姓首字母） | 变体常见于某些公司                |

## 命令

| 插件名称       | 生成格式示例（Anna Key） | 解释（常见企业规则）                    | OSCP应用场景                      |
| -------------- | ------------------------ | --------------------------------------- | --------------------------------- |
| **first.last** | anna.key                 | firstname.lastname（点分隔，全小写）    | 最常见（如Microsoft、Google风格） |
| **flast**      | akey                     | first initial + lastname（首字母+姓）   | 短用户名（如Unix旧系统）          |
| **firstl**     | annak                    | firstname + last initial（名+姓首字母） | 变体常见于某些公司                |

### 1)生成常见变体

```
username-anarchy -i names.txt --select-format first.last,flast,f.last
```

### 2)从单个名字生成

```
username-anarchy "First Last"  # 如 "John Doe"
```

### 3)列出所有格式

```
username-anarchy --list-formats
```

### 4)自动识别用户名格式

```
username-anarchy --recognise j.smith
```

### 5)指定国家姓名生成

```
username-anarchy --country china --auto > common_china.txt
```

### 6)添加后缀(@email.com)

```
username-anarchy -i names.txt --suffix @example.com
```

