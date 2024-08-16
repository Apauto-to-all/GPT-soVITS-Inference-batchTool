import shutil
import sys
import os

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from utils import GSV_utils


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
                with gr.Row():
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

                with gr.Row():
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

                with gr.Row():
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

    # 设置推理参数
    def showGSVInferenceSettingPage(self, demo: gr.Blocks):
        with gr.Tab(label="设置GPT-soVITS参数"):
            # 添加一个提示文本
            gr.Markdown("## 参数不多，支持随机")
            gr.Markdown("## 模型与情感选择")

            # 模型选择，下拉框，情感使用，多选框
            with gr.Row():
                model_name_input = gr.Dropdown(
                    label="选择模型名称",
                    interactive=True,
                    scale=1,
                )
                # 勾选需要使用的情感
                emotions_input = gr.CheckboxGroup(
                    label="选择需要使用的情感",
                    interactive=True,
                    scale=2,
                )
                # 切换模型，加载情感
                model_name_input.change(
                    self.reload_gr_GSV_emotions,
                    inputs=model_name_input,
                    outputs=emotions_input,
                )
            # 加载模型和上一次使用的模型
            demo.load(self.reload_gr_last_GSV_model, outputs=model_name_input)

            gr.Markdown("## 推理参数设置")
            speed_input = gr.Slider(
                label="语速（speed）",
                minimum=0.5,
                maximum=2.0,
                step=0.05,
                value=1.0,
                interactive=True,
                info="语速，默认1.0",
            )
            # top_k 设置，功能：top_k在推理的时候要挑出一个最好的token，但机器并不知道哪个是最好的。于是先按照top_k挑出前几个token
            with gr.Row():
                # 选择top_k
                top_k_input = gr.Slider(
                    label="采样（top_k）",
                    info="在推理的时候要挑出一个最好的token，但机器并不知道哪个是最好的。于是先按照top_k挑出前几个token",
                    step=1,
                    value=15,
                    maximum=100,
                    minimum=1,
                    interactive=True,
                    scale=3,
                )
                # 添加一个勾选框，用于设置top_k是否随机
                top_k_random = gr.Checkbox(
                    label="随机",
                    value=False,
                    interactive=True,
                    scale=1,
                )
                # 设置top_k随机的范围，2个数值输入框
                top_k_min = gr.Number(
                    label="范围最小值",
                    minimum=1,
                    maximum=100,
                    value=5,
                    step=1,
                    interactive=False,
                    visible=False,
                    scale=1,
                )
                top_k_max = gr.Number(
                    label="范围最大值",
                    minimum=1,
                    maximum=100,
                    value=20,
                    step=1,  # 步长
                    interactive=False,
                    visible=False,
                    scale=1,
                )
                # 如果勾选了随机，上面的数字输入框就可见，且可输入
                top_k_random.change(
                    self.update_random,
                    inputs=[top_k_random],
                    outputs=[top_k_min, top_k_max, top_k_input],
                )
            # top_p 设置，功能：top_p在top_k的基础上筛选token
            with gr.Row():
                top_p_input = gr.Slider(
                    label="采样（top_p）",
                    minimum=0,
                    maximum=2.0,
                    step=0.05,
                    value=0.8,
                    interactive=True,
                    info="top_p在top_k的基础上筛选token",
                    scale=3,
                )
                # 添加一个勾选框，用于设置top_p是否随机
                top_p_random = gr.Checkbox(
                    label="随机",
                    value=False,
                    interactive=True,
                    scale=1,
                )
                # 设置top_p随机的范围，2个数值输入框
                top_p_min = gr.Number(
                    label="范围最小值",
                    minimum=0,
                    maximum=2.0,
                    value=0.7,
                    step=0.05,  # 步长
                    interactive=False,
                    visible=False,
                    scale=1,
                )
                top_p_max = gr.Number(
                    label="范围最大值",
                    minimum=0,
                    maximum=2.0,
                    value=0.9,
                    step=0.05,  # 步长
                    interactive=False,
                    visible=False,
                    scale=1,
                )
                # 如果勾选了随机，上面的数字输入框就可见，且可输入
                top_p_random.change(
                    self.update_random,
                    inputs=[top_p_random],
                    outputs=[top_p_min, top_p_max, top_p_input],
                )

            # temperature 设置，功能：temperature控制随机性输出。
            with gr.Row():
                temperature_input = gr.Slider(
                    label="采样温度（temperature）",
                    minimum=0,
                    maximum=2.0,
                    step=0.05,
                    value=0.8,
                    interactive=True,
                    info="temperature控制随机性输出",
                    scale=3,
                )
                # 添加一个勾选框，用于设置temperature是否随机
                temperature_random = gr.Checkbox(
                    label="随机",
                    value=False,
                    interactive=True,
                    scale=1,
                )
                # 设置temperature随机的范围，2个数值输入框
                temperature_min = gr.Number(
                    label="范围最小值",
                    minimum=0,
                    maximum=2.0,
                    value=0.7,
                    step=0.05,  # 步长
                    interactive=False,
                    visible=False,
                    scale=1,
                )
                temperature_max = gr.Number(
                    label="范围最大值",
                    minimum=0,
                    maximum=2.0,
                    value=0.9,
                    step=0.05,  # 步长
                    interactive=False,
                    visible=False,
                    scale=1,
                )

                # temperature_random勾选框更新
                temperature_random.change(
                    self.update_random,
                    inputs=[temperature_random],
                    outputs=[
                        temperature_min,
                        temperature_max,
                        temperature_input,
                    ],
                )

            # 所有推理参数
            all_input = [
                emotions_input,
                speed_input,
                top_k_input,
                top_k_random,
                top_k_min,
                top_k_max,
                top_p_input,
                top_p_random,
                top_p_min,
                top_p_max,
                temperature_input,
                temperature_random,
                temperature_min,
                temperature_max,
            ]
            for i in all_input:
                i.change(
                    self.save_gr_GSV_inference_setting,
                    inputs=[model_name_input] + all_input,
                )
            model_name_input.change(
                self.reload_gr_GSV_inference_setting,
                inputs=model_name_input,
                outputs=all_input,
            )

        with gr.Tab(label="GPT-soVITS抽卡"):
            txt_input = gr.Textbox(label="输入文本（text）", lines=5)
            with gr.Row():
                # 输出语言设置，下拉框
                text_language = gr.Dropdown(
                    label="选择推理文本语言（text_language）",
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
                    value="多语种混合",
                    interactive=True,
                    info="输入文本的语言，默认多语种混合",
                )

                # 按什么切分文本，下拉框
                cut_method_input = gr.Dropdown(
                    label="切分方法（cut_punc）",
                    choices=[
                        "不切",
                        "凑四句一切",
                        "凑50字一切",
                        "按中文句号。切",
                        "按英文句号.切",
                        "按标点符号切",
                    ],
                    value="凑四句一切",
                    interactive=True,
                    info='文本切分符号设定, 默认为空, 以",.，。"字符串的方式传入',
                )

            # 连抽次数设置，抽卡按钮，停止按钮
            with gr.Row():
                illation_num_input = gr.Slider(
                    label="连抽次数",
                    minimum=1,
                    maximum=20,
                    step=1,
                )
                btn_generate = gr.Button("点击抽卡", variant="primary", size="lg")
                btn_stop = gr.Button("停停停！", variant="stop", size="lg")

            TTS_input = [
                txt_input,
                text_language,
                cut_method_input,
                illation_num_input,
            ]

            demo.load(
                self.reload_gr_GSV_inference_text,
                outputs=TTS_input,
            )
            for i in TTS_input:
                i.change(
                    self.save_last_save_text,
                    inputs=TTS_input,
                )

            # 输出音频组件
            output_audios = []  # 展示音频
            output_dudio_check = []  # 是否保存到项目
            # 按每行4个音频组件进行分组，并为每组创建一个Row
            for i in range(0, 20, 4):  # 从0开始，到20结束，步长为4
                with gr.Row():
                    for j in range(4):  # 每行4个音频组件
                        with gr.Column():
                            with gr.Row():
                                output_audios.append(
                                    gr.Audio(
                                        label=f"生成的音频{j+i+1}",
                                        type="filepath",
                                        visible=False if (i + j) != 0 else True,
                                        min_width=300,
                                        interactive=False,
                                    )
                                )
                                output_dudio_check.append(
                                    gr.Checkbox(
                                        label="",
                                        value=False,
                                        # container=False,  # 不显示外框
                                        # render=False,
                                        visible=False if (i + j) != 0 else True,
                                        min_width=1,
                                    )
                                )

            for i in range(20):
                output_dudio_check[i].change(
                    self.save_wav_file_to_project,
                    inputs=[output_dudio_check[i], output_audios[i]],
                )
