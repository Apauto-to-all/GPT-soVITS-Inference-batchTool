# 一个tab程序设置页面

import gradio as gr


class SettingPage:
    def __init__(self):
        pass

    def showSettingPage(self):
        # 显示一个
        with gr.Tab(label="项目管理"):
            with gr.Tab(label="项目管理1"):
                gr.Markdown("项目管理工具，用于展示项目的文件")
            with gr.Tab(label="项目管理2"):
                gr.Markdown("项目管理工具，用于展示项目的文件")
            with gr.Tab(label="项目管理3"):
                gr.Markdown("项目管理工具，用于展示项目的文件")
            with gr.Tab(label="项目管理4"):
                gr.Markdown("项目管理工具")

#     def test_setting_run(self):
#         with gr.Blocks() as demo:
#             self.show()
#         demo.launch(inbrowser=True)


# SettingPage().test_setting_run()
