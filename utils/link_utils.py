# 连接数据类的所有工具函数
import os
import sys

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import main_setting


class LinkUtils:
    def __init__(self):
        self.main_setting = main_setting.MainSetting()
