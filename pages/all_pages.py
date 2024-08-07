import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 整合所有页面，进行布局
from main_page import MainPage
from setting_page import SettingPage
import gradio as gr


class AllPages(MainPage):
    def __init__(self):
        super().__init__()

    def showAllPages(self):
        with gr.Blocks() as demo:
            gr.Markdown("# GPT-soVITS-Inference抽卡工具")
            # 2个tab页面
            self.showMainPage(demo)
            # 1个设置tab页面
            return demo

    def appRun(self):
        demo = self.showAllPages()
        demo.launch(
            server_name=self.main_data_utils.main_setting.app_local_host,  # 本地服务器地址
            server_port=self.main_data_utils.main_setting.app_local_port,  # 本地服务器端口
            inbrowser=self.main_data_utils.main_setting.auto_open_browser,  # 是否自动打开浏览器
        )
