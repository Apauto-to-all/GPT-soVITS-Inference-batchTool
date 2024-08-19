# 获取文件名储存格式
import re
import time


def get_filename(txt: str, max_len) -> str:
    # 获取当前时间戳
    timestamp = str(int(time.time()))
    # 如果txt是多行文本，合并为一行
    txt = txt.replace("\n", "_")
    txt = re.sub(r'[\\/:*?"<>|]', "_", txt)
    # 去除所有转义字符
    txt = re.sub(r"[\t\r]", "", txt)
    # 多余的字符用省略号代替
    if len(txt) > max_len:
        # 文件名中加入时间戳，确保每次都不同
        return timestamp + "_" + txt[:max_len] + "..."
    else:
        return timestamp + "_" + txt
