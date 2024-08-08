# 一个用于连接页面的中间件
import sys
import os

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import main_data, metadata_wav, proj_mgmt


class LinkPages:
    def __init__(self):
        self.main_data_utils = main_data.MainData()
        self.metadata_wav_utils = metadata_wav.MetadataWav()
        self.proj_mgmt_utils = proj_mgmt.ProjectManagement()
