WEB HTML 编辑小工具

# 文件说明

## ais\_mag.py

从Excel文件中读取文章列表，生成mag.json和文章框架到"posts"子目录中。逐个修改"posts"
中的HTML文件，然后运行`downimg.py`。

## downimg.py

自动下载HTML中的图片`<img>`到本地目录"images"。默认扫描脚本所在目录的"posts"子目录下
的HTML文件，如果要处理其它目录或文件，可以拖动目标目录或文件到脚本文件上。
