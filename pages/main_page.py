# 主要功能页面
import os
import shutil
import gradio as gr
from link_pages import LinkPages


class MainPage(LinkPages):
    def __init__(self):
        super().__init__()
        self.stop_flag = False  # 停止标志

    # 更新随机设置
    def update_random(self, is_random):
        if is_random:
            show = gr.update(interactive=True, visible=True)
        else:
            show = gr.update(interactive=True, visible=False)
        return (
            show,
            show,
            gr.update(interactive=False) if is_random else gr.update(interactive=True),
        )

    def showMainPage(self, demo: gr.Blocks):
        if self.main_data_utils.main_setting.all_models_emotions == -1:
            with gr.Tab(label="检测到后端服务未启动"):
                gr.Markdown("# 检测到GPT-soVITS-Inference后端服务未启动")
                gr.Markdown(
                    "## 本程序依赖于GPT-soVITS-Inference的API接口，启动后端后，再重启本程序"
                )
                gr.Markdown(
                    "## 本程序默认的角色列表URL地址为：http://127.0.0.1:5000/character_list"
                )
                gr.Markdown(
                    "## 本程序默认的文本转语音URL地址为：http://127.0.0.1:5000/tts"
                )
                gr.Markdown(
                    f"## 如果你切换了后端服务的地址，或者端口，需要在 {self.main_data_utils.main_setting.main_data_path} 中修改"
                )
            return
        with gr.Tab(label="设置GPT-soVITS-Inference参数"):
            # 添加一个提示文本
            gr.Markdown(
                "## 提示：设置完随机参数后（设置会自动保存），切换到“开始抽卡”标签页，点击“点击抽卡”按钮即可开始使用"
            )
            gr.Markdown("## 模型与情感选择")

            # 模型选择，下拉框，情感使用，多选框
            with gr.Row():
                model_name_input = gr.Dropdown(
                    label="选择模型名称",
                    choices=self.main_data_utils.main_setting.all_models,
                )
                with gr.Column():
                    # 全选box
                    select_all = gr.Checkbox(label="全选", value=False)

                    # 勾选需要使用的情感

                    emotions_input = gr.CheckboxGroup(
                        label="选择需要使用的情感", interactive=True
                    )

                    # 全选box更新时，更新emotions_input的选项
                    def update_emotions_all(select_all, model_name):
                        if select_all:
                            return gr.update(
                                value=self.main_data_utils.main_setting.all_models_emotions[
                                    model_name
                                ]
                            )
                        else:
                            return gr.update(value=[])

                    select_all.change(
                        update_emotions_all,
                        inputs=[select_all, model_name_input],
                        outputs=[emotions_input],
                    )

                    # model_name_input更新时，更新emotions_input的选项
                    def update_emotions(model_name):
                        return gr.update(
                            choices=self.main_data_utils.main_setting.all_models_emotions[
                                model_name
                            ]
                        )

                    model_name_input.change(
                        update_emotions,
                        inputs=[model_name_input],
                        outputs=[emotions_input],
                    )

            # 添加其他随机设置
            gr.Markdown("## 其他设置")
            with gr.Row():
                # 简单设置
                with gr.Column():
                    gr.Markdown("### 基础设置")
                    # 速度设置，滑块
                    speed_input = gr.Slider(
                        label="语速（speed）",
                        minimum=0.5,
                        maximum=2.0,
                        step=0.05,
                        value=1.0,
                        interactive=True,
                        info="语速，默认1.0",
                    )

                    # max_cut_length 设置，功能：最大切分长度，滑块
                    with gr.Row():
                        max_cut_length_input = gr.Slider(
                            label="最大切分长度（max_cut_length）",
                            minimum=5,
                            maximum=1000,
                            step=1,
                            min_width=400,
                            value=50,
                            interactive=True,
                            info="最大切分长度，默认50",
                        )
                        # 添加一个勾选框，用于设置max_cut_length是否随机
                        max_cut_length_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置max_cut_length随机的范围，2个数值输入框
                        max_cut_length_min = gr.Number(
                            label="范围最小值",  # 标签
                            minimum=5,  # 最小值
                            maximum=1000,  # 最大值
                            value=50,  # 默认值
                            step=1,  # 步长
                            interactive=False,  # 不可交互
                            visible=False,  # 不可见
                            min_width=100,  # 最小宽度
                        )
                        max_cut_length_max = gr.Number(
                            label="范围最大值",  # 标签
                            minimum=5,  # 最小值
                            maximum=1000,
                            value=50,
                            step=1,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )

                        # 如果勾选了随机，上面的数字输入框就可见，且可输入
                        max_cut_length_random.change(
                            self.update_random,
                            inputs=[max_cut_length_random],
                            outputs=[
                                max_cut_length_min,
                                max_cut_length_max,
                                max_cut_length_input,
                            ],
                        )

                    # batch_size 设置，功能：批处理大小，滑块
                    with gr.Row():
                        batch_size_input = gr.Slider(
                            label="批处理大小（batch_size）",
                            minimum=1,
                            maximum=100,
                            step=1,
                            min_width=400,
                            value=10,
                            interactive=True,
                            info="批处理大小，默认10",
                        )
                        # 添加一个勾选框，用于设置batch_size是否随机
                        batch_size_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置batch_size随机的范围，2个数值输入框
                        batch_size_min = gr.Number(
                            label="范围最小值",  # 标签
                            minimum=1,  # 最小值
                            maximum=100,  # 最大值
                            value=10,  # 默认值
                            step=1,  # 步长
                            interactive=False,  # 不可交互
                            visible=False,  # 不可见
                            min_width=100,  # 最小宽度
                        )
                        batch_size_max = gr.Number(
                            label="范围最大值",
                            minimum=1,
                            maximum=100,
                            value=10,
                            step=1,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )

                        # 如果勾选了随机，上面的数字输入框就可见，且可输入，并禁止原来的滑块
                        batch_size_random.change(
                            self.update_random,
                            inputs=[batch_size_random],
                            outputs=[
                                batch_size_min,
                                batch_size_max,
                                batch_size_input,
                            ],
                        )

                    gr.Markdown("### 一般不需要动的设置")

                    # task_type类型
                    task_type_input = gr.Textbox(
                        label="任务类型（task_type）",
                        value="text",
                        interactive=False,
                        info="任务类型，默认text，不提供交互",
                    )
                    # format设置，下拉框
                    format_input = gr.Dropdown(
                        label="保存格式（format）",
                        choices=["wav"],
                        value="wav",  # 保存格式，默认为wav。
                        interactive=True,
                        info="格式，默认wav，基本你随意指定，不支持会重新返回wav（本程序只提供wav文件格式）",
                    )

                    # sample_rate 设置，滑块
                    sample_rate_input = gr.Slider(
                        label="采样率（sample_rate）",
                        minimum=8000,
                        maximum=48000,
                        step=1000,
                        value=32000,
                        interactive=True,
                        info="采样率，默认32000",
                    )

                    # stream设置，True or False
                    stream_input = gr.Checkbox(
                        label="是否流式传输（stream）",
                        value=False,
                        interactive=False,
                        info="是否流式传输，为true时，会按句返回音频，默认为false。（本程序是目的是抽卡，没必要）",
                    )

                    # save_temp设置，是否保存临时文件
                    save_temp_input = gr.Checkbox(
                        label="是否保存临时文件（save_temp）",
                        value=False,
                        interactive=True,
                        info="是否保存临时文件，为true时，后端会保存生成的音频，下次相同请求会直接返回该数据，默认为false。（对于抽卡程序也无必要）",
                    )

                    # prompt_text设置，参考的文本，但包含在情感列表中
                    prompt_text_input = gr.Textbox(
                        label="参考文本（prompt_text）",
                        value="",
                        interactive=False,
                        info="参考文本，应该包含在情感列表中，不提供交互",
                    )

                    # prompt_language设置，功能：参考文本的语言，应该也包含在情感列表中
                    prompt_language_input = gr.Dropdown(
                        label="参考文本语言（prompt_language）",
                        choices=["auto"],
                        value="auto",
                        interactive=False,
                        info="参考文本的语言，应该也包含在情感列表中，不提供交互",
                    )

                # 复杂设置
                with gr.Column():
                    gr.Markdown("### 高级设置")
                    # parallel_infer 设置，功能：是否并行推理，为true时，会加速很多，默认为true。
                    parallel_infer_input = gr.Checkbox(
                        label="是否并行推理（parallel_infer）",
                        value=True,
                        interactive=True,
                        info="是否并行推理，为true时，会加速很多，默认为true",
                    )
                    # seed，功能：随机种子，默认为-1。
                    seed_input = gr.Number(
                        label="随机种子（seed）",
                        value=-1,
                        interactive=True,
                        info="种子，默认为-1，表示随机",
                    )

                    # top_k 设置，功能：在推理的时候要挑出一个最好的token，但机器并不知道哪个是最好的。于是先按照top_k挑出前几个token
                    with gr.Row():
                        top_k_input = gr.Slider(
                            label="采样（top_k）",
                            minimum=1,
                            maximum=100,
                            step=1,
                            value=10,
                            interactive=True,
                            min_width=400,
                            info="在推理的时候要挑出一个最好的token，但机器并不知道哪个是最好的。于是先按照top_k挑出前几个token",
                        )
                        # 添加一个勾选框，用于设置top_k是否随机
                        top_k_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置top_k随机的范围，2个数值输入框
                        top_k_min = gr.Number(
                            label="范围最小值",
                            minimum=1,
                            maximum=100,
                            value=1,
                            step=1,
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )
                        top_k_max = gr.Number(
                            label="范围最大值",
                            minimum=1,
                            maximum=100,
                            value=10,
                            step=1,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
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
                            step=0.01,
                            value=0.8,
                            interactive=True,
                            min_width=400,
                            info="top_p在top_k的基础上筛选token",
                        )
                        # 添加一个勾选框，用于设置top_p是否随机
                        top_p_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置top_p随机的范围，2个数值输入框
                        top_p_min = gr.Number(
                            label="范围最小值",
                            minimum=0,
                            maximum=2.0,
                            value=0.7,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )
                        top_p_max = gr.Number(
                            label="范围最大值",
                            minimum=0,
                            maximum=2.0,
                            value=0.9,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
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
                            step=0.01,
                            value=0.8,
                            interactive=True,
                            min_width=400,
                            info="temperature控制随机性输出",
                        )
                        # 添加一个勾选框，用于设置temperature是否随机
                        temperature_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置temperature随机的范围，2个数值输入框
                        temperature_min = gr.Number(
                            label="范围最小值",
                            minimum=0,
                            maximum=2.0,
                            value=0.7,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )
                        temperature_max = gr.Number(
                            label="范围最大值",
                            minimum=0,
                            maximum=2.0,
                            value=0.9,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
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

                    # repetition_penalty 设置，功能：重复惩罚，数值越大，越不容易重复，默认为1.35。
                    with gr.Row():
                        repetition_penalty_input = gr.Slider(
                            label="重复惩罚（repetition_penalty）",
                            minimum=0,
                            maximum=5.0,
                            step=0.01,
                            value=1.35,
                            interactive=True,
                            min_width=400,
                            info="重复惩罚，数值越大，越不容易重复，默认为1.35",
                        )
                        # 添加一个勾选框，用于设置repetition_penalty是否随机
                        repetition_penalty_random = gr.Checkbox(
                            label="随机",
                            value=False,
                            interactive=True,
                            min_width=50,
                        )
                        # 设置repetition_penalty随机的范围，2个数值输入框
                        repetition_penalty_min = gr.Number(
                            label="范围最小值",
                            minimum=0,
                            maximum=5.0,
                            value=1.35,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )
                        repetition_penalty_max = gr.Number(
                            label="范围最大值",
                            minimum=0,
                            maximum=5.0,
                            value=1.35,
                            step=0.01,  # 步长
                            interactive=False,
                            visible=False,
                            min_width=100,
                        )

                        # repetition_penalty_random勾选框更新
                        repetition_penalty_random.change(
                            self.update_random,
                            inputs=[repetition_penalty_random],
                            outputs=[
                                repetition_penalty_min,
                                repetition_penalty_max,
                                repetition_penalty_input,
                            ],
                        )

        with gr.Tab(label="开始抽卡"):
            txt_input = gr.Textbox(label="输入文本", lines=5)
            with gr.Row():
                # 输出语言设置，下拉框
                text_language = gr.Dropdown(
                    label="选择输出语言（text_language）",
                    choices=[
                        "中文",
                        "英文",
                        "日文",
                        "中英混合",
                        "日英混合",
                        "多语种混合",
                    ],
                    value="多语种混合",
                    interactive=True,
                    info="输入文本的语言，默认多语种混合",
                )

                # cut_method 设置，功能：切分方法，下拉框
                cut_method_input = gr.Dropdown(
                    label="切分方法（cut_method）",
                    choices=[
                        "智能切分",
                        "仅凭换行切分",
                        "凑四句一切",
                        "凑50字一切",
                        "按中文句号。切",
                        "按英文句号.切",
                        "按标点符号切",
                    ],
                    value="智能切分",
                    interactive=True,
                    info="切分方法，auto_cut：智能切分，cut0：仅凭换行切分，cut1：凑四句一切，cut2：凑50字一切，cut3：按中文句号。切，cut4：按英文句号.切，cut5：按标点符号切",
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

            def save_wav_file_to_project(output_dudio_check, audio_file_path):
                if not audio_file_path:
                    if output_dudio_check:
                        gr.Warning("未生成音频文件，请检查！")
                    return
                project_folder_path = (
                    self.proj_mgmt_utils.proj_setting.get_sub_project_path_from_last()
                )
                if not project_folder_path:
                    gr.Warning("未选择子项目，请检查")
                    return
                # 将音频文件移动到项目文件夹
                if not os.path.exists(project_folder_path):
                    os.makedirs(project_folder_path, exist_ok=True)
                # 获取源文件的文件名
                file_name = os.path.basename(audio_file_path)
                if output_dudio_check:  # 如果勾选
                    # copy2可以复制文件的元数据
                    shutil.copy2(audio_file_path, project_folder_path)
                else:  # 如果取消勾选，就删除目标文件
                    # 定义目标文件路径
                    target_path = os.path.join(project_folder_path, file_name)
                    if os.path.exists(target_path):
                        os.remove(target_path)

            for i in range(20):
                output_dudio_check[i].change(
                    save_wav_file_to_project,
                    inputs=[output_dudio_check[i], output_audios[i]],
                )

            # 点击按钮后，调用stop_generation函数，停止生成音频
            def stop_generation():
                self.stop_flag = True

            # 绑定按钮的click事件
            btn_stop.click(stop_generation)

            # 点击按钮后，调用update_audios函数，传入输入组件和输出组件
            async def update_audios(model_name, txt, illation_num):
                self.stop_flag = False
                # 初始化输出结果
                results_audio = [
                    gr.update(visible=True if _ == 0 else False, value=None)
                    for _ in range(20)
                ]
                results_check = [
                    gr.update(visible=True if _ == 0 else False, value=False)
                    for _ in range(20)
                ]
                yield results_audio + results_check
                i = 0
                async for wav_file_path in self.main_data_utils.interface(
                    model_name, txt, illation_num
                ):
                    if self.stop_flag:
                        break
                    if not wav_file_path:
                        break
                    if i < 20:
                        results_audio[i] = gr.update(value=wav_file_path, visible=True)
                        results_check[i] = gr.update(visible=True)
                        yield results_audio + results_check
                    else:
                        break
                    i += 1

            # 绑定抽卡按钮的click事件
            btn_generate.click(
                update_audios,
                inputs=[model_name_input, txt_input, illation_num_input],
                outputs=output_audios + output_dudio_check,
            )

        # 定义一个列表，包含所有组件，除了模型，文本，连抽次数
        all_input = [
            model_name_input,
            illation_num_input,
            txt_input,
            emotions_input,
            format_input,
            sample_rate_input,
            speed_input,
            stream_input,
            save_temp_input,
            prompt_text_input,
            prompt_language_input,
            text_language,
            batch_size_input,
            batch_size_random,
            batch_size_min,
            batch_size_max,
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
            cut_method_input,
            max_cut_length_input,
            max_cut_length_random,
            max_cut_length_min,
            max_cut_length_max,
            seed_input,
            parallel_infer_input,
            repetition_penalty_input,
            repetition_penalty_random,
            repetition_penalty_min,
            repetition_penalty_max,
            task_type_input,
        ]

        # 保存所有数据，除了最后使用的模型，如果模型改变，才保存最后的模型
        def save_all_data(
            model_name,
            illation_num,
            txt,
            emotions,
            format,
            sample_rate,
            speed,
            stream,
            save_temp,
            prompt_text,
            prompt_language,
            text_language,
            # 随机参数batch_size
            betch_size,
            betch_size_random,
            batch_size_min,
            batch_size_max,
            # 随机参数top_k
            top_k,
            top_k_random,
            top_k_min,
            top_k_max,
            # 随机参数top_p
            top_p,
            top_p_random,
            top_p_min,
            top_p_max,
            # 随机参数temperature
            temperature,
            temperature_random,
            temperature_min,
            temperature_max,
            cut_method,
            # 随机参数max_cut_length
            max_cut_length,
            max_cut_length_random,
            max_cut_length_min,
            max_cut_length_max,
            seed,
            parallel_infer,
            # 随机参数repetition_penalty
            repetition_penalty,
            repetition_penalty_random,
            repetition_penalty_min,
            repetition_penalty_max,
            task_type,
        ):
            if not model_name:
                return
            betch_size_list = [
                betch_size_random,
                betch_size,
                batch_size_min,
                batch_size_max,
            ]
            top_k_list = [top_k_random, top_k, top_k_min, top_k_max]
            top_p_list = [top_p_random, top_p, top_p_min, top_p_max]
            temperature_list = [
                temperature_random,
                temperature,
                temperature_min,
                temperature_max,
            ]
            max_cut_length_list = [
                max_cut_length_random,
                max_cut_length,
                max_cut_length_min,
                max_cut_length_max,
            ]
            repetition_penalty_list = [
                repetition_penalty_random,
                repetition_penalty,
                repetition_penalty_min,
                repetition_penalty_max,
            ]
            all_data = {
                "model_name": model_name,
                "emotions": emotions,
                "format": format,
                "sample_rate": sample_rate,
                "speed": speed,
                "stream": stream,
                "save_temp": save_temp,
                "prompt_text": prompt_text,
                "prompt_language": prompt_language,
                "text_language": text_language,
                "batch_size": betch_size_list,  # 随机参数batch_size
                "top_k": top_k_list,  # 随机参数top_k
                "top_p": top_p_list,  # 随机参数top_p
                "temperature": temperature_list,  # 随机参数temperature
                "cut_method": cut_method,
                "max_cut_length": max_cut_length_list,  # 随机参数max_cut_length
                "seed": seed,
                "parallel_infer": "true" if parallel_infer else "false",
                "repetition_penalty": repetition_penalty_list,  # 随机参数repetition_penalty
                "task_type": task_type,
            }
            self.main_data_utils.save_illation_num(illation_num)
            self.main_data_utils.save_test_txt(txt)
            self.main_data_utils.save_all_data(all_data)

        # 加载所有数据
        # 加载页面时，自动加载model配置文件的内容
        def reload_model_all_data(model_name=None):
            if model_name:  # 如果模型名称不为空
                self.main_data_utils.save_last_model(model_name)  # 保存模型名称
            else:
                model_name = self.main_data_utils.get_last_model(
                    self.main_data_utils.main_setting.all_models
                )  # 获取最后使用的模型名称
            illation_num_input = self.main_data_utils.get_illation_num()  # 获取迭代次数
            txt_input = self.main_data_utils.get_test_txt()  # 获取测试文本
            # 读取模型的所有数据
            all_data = self.main_data_utils.get_all_data(model_name)
            emotions_input = all_data.get("emotions", [])
            format_input = all_data.get("format", "wav")
            sample_rate_input = all_data.get("sample_rate", 32000)
            speed_input = all_data.get("speed", 1.0)
            stream_input = all_data.get("stream", False)
            save_temp_input = all_data.get("save_temp", False)
            prompt_text_input = all_data.get("prompt_text", "")
            prompt_language_input = all_data.get("prompt_language", "auto")
            text_language_input = all_data.get("text_language", "多语种混合")
            # 随机参数batch_size
            batch_size_list = all_data.get("batch_size", [False, 10, 5, 15])
            batch_size_input = batch_size_list[1]
            batch_size_random = batch_size_list[0]
            batch_size_min = batch_size_list[2]
            batch_size_max = batch_size_list[3]
            # 随机参数top_k
            top_k_list = all_data.get("top_k", [False, 5, 1, 10])
            top_k_input = top_k_list[1]
            top_k_random = top_k_list[0]
            top_k_min = top_k_list[2]
            top_k_max = top_k_list[3]
            # 随机参数top_p
            top_p_list = all_data.get("top_p", [False, 0.8, 0.7, 0.9])
            top_p_input = top_p_list[1]
            top_p_random = top_p_list[0]
            top_p_min = top_p_list[2]
            top_p_max = top_p_list[3]
            # 随机参数temperature
            temperature_list = all_data.get("temperature", [False, 0.8, 0.7, 0.9])
            temperature_input = temperature_list[1]
            temperature_random = temperature_list[0]
            temperature_min = temperature_list[2]
            temperature_max = temperature_list[3]
            cut_method_input = all_data.get("cut_method", "智能切分")
            # 随机参数max_cut_length
            max_cut_length_list = all_data.get("max_cut_length", [False, 50, 50, 50])
            max_cut_length_input = max_cut_length_list[1]
            max_cut_length_random = max_cut_length_list[0]
            max_cut_length_min = max_cut_length_list[2]
            max_cut_length_max = max_cut_length_list[3]
            seed_input = all_data.get("seed", -1)
            parallel_infer_input = (
                "true" if all_data.get("parallel_infer", "true") == "true" else "false"
            )
            # 随机参数repetition_penalty
            repetition_penalty_list = all_data.get(
                "repetition_penalty", [False, 1.35, 1.35, 1.35]
            )
            repetition_penalty_input = repetition_penalty_list[1]
            repetition_penalty_random = repetition_penalty_list[0]
            repetition_penalty_min = repetition_penalty_list[2]
            repetition_penalty_max = repetition_penalty_list[3]
            task_type_input = all_data.get("task_type", "text")

            return (
                model_name,
                illation_num_input,
                txt_input,
                emotions_input,
                format_input,
                sample_rate_input,
                speed_input,
                stream_input,
                save_temp_input,
                prompt_text_input,
                prompt_language_input,
                text_language_input,
                batch_size_input,
                batch_size_random,
                batch_size_min,
                batch_size_max,
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
                cut_method_input,
                max_cut_length_input,
                max_cut_length_random,
                max_cut_length_min,
                max_cut_length_max,
                seed_input,
                parallel_infer_input,
                repetition_penalty_input,
                repetition_penalty_random,
                repetition_penalty_min,
                repetition_penalty_max,
                task_type_input,
            )

        # 当模型名称改变时，重新加载所有数据，并保存模型名称
        model_name_input.change(
            reload_model_all_data,
            inputs=[model_name_input],  # 模型添加到输入
            outputs=all_input,
        )

        # 当打开页面时，自动加载上次使用的模型和模型的参数数据
        demo.load(
            reload_model_all_data,
            outputs=all_input,
        )

        # 保存所有数据，当所有数据改变时，保存所有数据，除了模型改变（防止覆盖）
        for input_element in all_input[1:]:
            input_element.change(
                save_all_data,
                inputs=all_input,
            )
