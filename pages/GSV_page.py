import sys
import os

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import gradio as gr
from tkinter import Tk, filedialog
from utils import GSV_utils

"""
    "top_k": 20,
    "top_p": 0.6,
    "temperature": 0.6,
    "speed": 1
"""


class GSVPage(GSV_utils.GSVUtils):
    def __init__(self):
        super().__init__()

    def showGSVSettingPage(self, demo: gr.Blocks):
        button_save = gr.Button(
            value="保存设置",
            variant="primary",
            size="sm",
        )
        with gr.Tab(label="GPT-soVITS设置"):
            # 选择GSV文件夹路径
            self.GSV_path_input = gr.Textbox(
                label="GPT-soVITS路径",
                placeholder="请点击按钮选择GPT-soVITS路径",
                interactive=False,
            )
            button_select_GSV_path = gr.Button(
                value="选择GPT-soVITS路径",
                variant="primary",
                size="sm",
            )

            # python环境，先检测默认，如果没有则选择其他
            self.python_embedded_path_input = gr.Textbox(
                label="Python环境",
                placeholder="请点击按钮选择Python环境",
                interactive=False,
            )
            python_version = gr.Textbox(
                label="Python版本",
                placeholder="Python版本",
                interactive=False,
            )
            self.python_embedded_path_input.change(
                self.get_GSV_python_embedded_version,
                outputs=python_version,
            )
            button_select_python_embedded_path = gr.Button(
                value="选择Python环境",
                variant="primary",
                size="sm",
            )
            button_select_python_embedded_path.click(
                self.select_python_embedded_path,
                outputs=self.python_embedded_path_input,
                show_progress="hidden",
            )

            # 选择GPT-soVITS路径，并保存：GPT-soVITS路径，Python环境
            button_select_GSV_path.click(
                self.select_GSV_Folder,
                outputs=[self.GSV_path_input, self.python_embedded_path_input],
                show_progress="hidden",
            )
