# xiaohuo_tools
一些小工具
# 目录
## mergelog.py
```
Usage: python mergelog.py [options] arg, use -h to get help info

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -l LOG_LIST, --log_list=LOG_LIST
                        需要进行合并的log列表多个文件路径用‘,’分隔
  -o OUTPUT, --output=OUTPUT
                        指定输入合并后的日志路径
```
- 用来根据日志的日期时间顺序合并多个给定的日志，并保留哪一行来自于那个日志文件信息
- 不存在时间的日志行跟随上文