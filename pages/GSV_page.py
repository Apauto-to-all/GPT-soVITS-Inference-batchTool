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
        # button_save = gr.Button(
        #     value="保存设置",
        #     variant="primary",
        #     size="sm",
        # )
        with gr.Tab(label="GPT-soVITS设置"):
            gr.Markdown("### 选择GPT-soVITS目录与Python环境")
            with gr.Row():
                # 选择GSV文件夹路径
                GSV_path_input = gr.Textbox(
                    label="GPT-soVITS路径",
                    placeholder="请点击按钮选择GPT-soVITS路径",
                    interactive=False,
                )
                button_select_GSV_path = gr.Button(
                    value="选择GPT-soVITS路径",
                    variant="primary",
                    size="sm",
                )

            with gr.Row():
                # python环境，先检测默认，如果没有则选择其他
                python_embedded_path_input = gr.Textbox(
                    label="Python环境",
                    placeholder="请点击按钮选择Python环境",
                    interactive=False,
                )
                python_version = gr.Textbox(
                    label="Python版本",
                    placeholder="Python版本",
                    interactive=False,
                )
                python_embedded_path_input.change(
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
                outputs=python_embedded_path_input,
                show_progress="hidden",
            )

            # 选择GPT-soVITS路径，并保存：GPT-soVITS路径，Python环境
            button_select_GSV_path.click(
                self.select_GSV_Folder,
                outputs=[GSV_path_input, python_embedded_path_input],
                show_progress="hidden",
            )
            demo.load(
                self.reload_GSV_path_python,
                outputs=[GSV_path_input, python_embedded_path_input],
            )
        with gr.Tab(label="GPT-soVITS的API设置"):
            with gr.Column():
                gr.Markdown("### GPT-soVITS的API设置，刷新页面查看最新设置")
                GSV_api_file_path_input = gr.Textbox(
                    label="API配置文件路径",
                    placeholder="如果没有文件地址，请重新选择GPT-soVITS目录",
                    interactive=False,
                )
                # GPT-soVITS 的API绑定地址
                GSV_address_input = gr.Textbox(
                    label="API绑定地址",
                    info="绑定地址, 默认127.0.0.1",
                    interactive=True,
                )
                # GPT-soVITS 的API绑定端口
                GSV_port_input = gr.Number(
                    label="API绑定端口",
                    info="绑定端口, 默认9880",
                    step=1,
                    maximum=65535,
                    minimum=1,
                    interactive=True,
                )
                # GPT-soVITS 的API推理设备
                GSV_device_input = gr.Dropdown(
                    label="API推理设备",
                    info="`推理设备, cuda,cpu",
                    choices=["使用默认", "cuda", "cpu"],
                )
                # GPT-soVITS 的API精度
                GSV_precision_input = gr.Dropdown(
                    label="API精度",
                    info="选择半精度（hp）或全精度（fh）",
                    choices=["使用默认", "hp", "fp"],
                )
                # GPT-soVITS 的API流式返回模式
                GSV_stream_mode_input = gr.Dropdown(
                    label="API流式返回模式",
                    info='流式返回模式, 默认不启用, "close","c", "normal","n", "keepalive","k"，本程序不使用流式，不设置',
                    choices=["close", "normal", "keepalive"],
                    interactive=False,
                )
                # GPT-soVITS 的API返回的音频编码格式
                GSV_media_type_input = gr.Dropdown(
                    label="API返回的音频编码格式",
                    info='返回的音频编码格式, 流式默认ogg, 非流式默认wav, "wav", "ogg", "aac"，本程序不使用流式，不设置',
                    choices=["wav", "ogg", "aac"],
                    interactive=False,
                )
                # GPT-soVITS 的API cnhubert路径
                GSV_hubert_path_input = gr.Textbox(
                    label="API cnhubert路径",
                    info="cnhubert路径, 不设置",
                    interactive=False,
                )
                # GPT-soVITS 的API bert路径
                GSV_bert_path_input = gr.Textbox(
                    label="API bert路径",
                    info="bert路径，不设置",
                    interactive=False,
                )

            demo.load(
                self.reload_GSV_api_data,
                outputs=[
                    GSV_api_file_path_input,
                    GSV_address_input,
                    GSV_port_input,
                    GSV_device_input,
                    GSV_precision_input,
                    GSV_stream_mode_input,
                    GSV_media_type_input,
                    GSV_hubert_path_input,
                    GSV_bert_path_input,
                ],
            )
