import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 整合所有页面，进行布局
from main_page import MainPage
from setting_page import SettingPage
from proj_page import ProjPage
from GSV_page import GSVPage
import gradio as gr


class AllPages:
    def __init__(self):
        self.main_page = MainPage()
        self.setting_page = SettingPage()
        self.proj_page = ProjPage()
        self.GSV_page = GSVPage()

    def showAllPages(self):
        with gr.Blocks(title="抽卡工具") as demo:
            gr.Markdown("# GPT-soVITS-Inference抽卡工具")
            # 在顶部显示当前使用项目
            self.proj_page.showSelectProj(demo)
            # 2个tab页面，主页面
            self.main_page.showMainPage(demo)
            # 一个GSV模型管理页面
            self.GSV_page.showGSVmodelManagePage(demo)
            # 一个GSV推理参数设置页面
            self.GSV_page.showGSVInferenceSettingPage(demo)
            # 1个项目管理页面
            self.proj_page.showProjMgmt(demo)
            with gr.Tab(label="设置"):
                with gr.Tab(label="GPT-soVITS-Inference设置"):
                    self.setting_page.showSettingPage(demo)
                with gr.Tab(label="GPT-soVITS设置"):
                    self.GSV_page.showGSVSettingPage(demo)
            return demo

    def appRun(self):
        demo = self.showAllPages()
        demo.launch(
            server_name=self.main_page.main_data_utils.main_setting.app_local_host,  # 本地服务器地址
            server_port=self.main_page.main_data_utils.main_setting.app_local_port,  # 本地服务器端口
            inbrowser=self.main_page.main_data_utils.main_setting.auto_open_browser,  # 是否自动打开浏览器
        )
