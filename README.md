# WEB HTML 编辑小工具

用于辅助制作 ArcSoft AISG 内刊。

# 文件说明

- `ais_mag.py`: 从Excel文件中读取文章列表，生成`mag.json`和文章框架到`posts`子目录中。
- `downimg.py`: 自动下载HTML中的图片`<img>`到本地目录`images`。


# 步骤

1. 拖动包含规则文章列表的Excel文件到`ais_mag.py`，生成`mag.json`和文章框架到`posts`子目录中。
2. 逐个修改`posts`中的HTML文件。
3. 拖动`posts`目录到`downimg.py`，下载`posts`目录下HTML文件需要的图片到`posts/images`目录。
4. 默认`downimg.py`扫描`posts`子目录下的HTML文件，如果要处理其它目录或文件，可以拖动目标目录或文件到脚本文件上。

