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

    # 显示GSV的一些设置
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

    # 模型感情界面管理界面
    def showGSVmodelManagePage(self, demo: gr.Blocks):
        with gr.Tab(label="GPT-soVITS训练的模型管理界面"):
            gr.Markdown(
                "### 模型管理，在model文件夹下，创建一个文件夹（文件名就是你模型的文件名），里面放训练好的SoVITS模型和GPT模型，然后放一些参考音频文件，完成后回到该页面，点击“重新加载模型”按钮。"
            )
            gr.Markdown(
                "### 参考音频已自动分配完成，在需要使用的参考音频前，请输入情感，参考文字，参考语言。在所有步骤完成后，点击“保存模型”按钮。"
            )
            with gr.Row():
                with gr.Column():
                    # 加载model文件夹下的所有模型
                    all_model_input = gr.Dropdown(
                        label="模型选择",
                        interactive=True,
                    )
                    # 加载模型按钮
                    button_select_model = gr.Button(
                        value="重新加载模型",
                        variant="primary",
                        size="sm",
                    )
                    button_select_model.click(
                        self.reload_gr_GSV_model,
                        outputs=all_model_input,
                    )
                with gr.Column():
                    # 加载模型文件夹下的GPT模型
                    all_GSV_model = gr.Dropdown(
                        label="GPT模型选择",
                        interactive=True,
                    )
                    # 加载模型文件夹下的SoVITS模型
                    all_SoVITS_model = gr.Dropdown(
                        label="SoVITS模型选择",
                        interactive=True,
                    )
                button_save_all = gr.Button(
                    value="保存模型",
                    variant="primary",
                    size="sm",
                )
            # 所有参考音频情感
            all_audio_emotion = []
            # 加载模型文件夹下的参考音频
            all_audio_input = []
            # 所有音频文件的参考文字
            all_audio_text = []
            # 参考音频语言
            all_audio_language = []
            # 预览参考音频
            all_audio_preview = []
            # 布局参考音频
            for i in range(self.show_audio_num):
                with gr.Column():
                    with gr.Row():
                        all_audio_emotion.append(
                            gr.Textbox(
                                label=f"参考音频情感{i+1}",
                                placeholder="输入该参考音频情感",
                                interactive=True,
                                visible=False,
                                scale=1,
                            )
                        )
                        with gr.Column(scale=4):
                            with gr.Row():
                                all_audio_input.append(
                                    gr.Textbox(
                                        label=f"参考音频{i+1}",
                                        visible=False,
                                        interactive=False,
                                        scale=3,
                                    )
                                )
                                all_audio_language.append(
                                    gr.Dropdown(
                                        label=f"参考音频语言{i+1}",
                                        choices=[
                                            "中文",
                                            "粤语",
                                            "英文",
                                            "日文",
                                            "韩文",
                                            "中英混合",
                                            "粤英混合",
                                            "日英混合",
                                            "韩英混合",
                                            "多语种混合",
                                            "多语种混合(粤语)",
                                        ],
                                        interactive=True,
                                        visible=False,
                                        scale=1,
                                    )
                                )
                            all_audio_text.append(
                                gr.Textbox(
                                    label=f"参考音频文字{i+1}",
                                    placeholder="输入该参考音频文字",
                                    interactive=True,
                                    visible=False,
                                )
                            )
                        all_audio_preview.append(
                            gr.Audio(
                                label=f"参考音频{i+1}预览",
                                type="filepath",
                                interactive=False,
                                visible=False,
                                scale=1,
                            )
                        )

            all_model_input.change(
                self.reload_GSV_model_audio,
                inputs=all_model_input,
                outputs=[
                    all_GSV_model,
                    all_SoVITS_model,
                ]
                + all_audio_emotion
                + all_audio_input
                + all_audio_text
                + all_audio_language
                + all_audio_preview,
            )

            button_save_all.click(
                self.save_all_GSV_model,
                inputs=[
                    all_model_input,
                    all_GSV_model,
                    all_SoVITS_model,
                ]
                + all_audio_emotion
                + all_audio_input
                + all_audio_text
                + all_audio_language,
            )