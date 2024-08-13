# 一个tab程序设置页面
import json
import os
import gradio as gr
from link_pages import LinkPages


class SettingPage(LinkPages):
    def __init__(self):
        super().__init__()

    def showSettingPage(self, demo):
        # 显示一个
        gr.Markdown(
            "修改设置后，需要点击“保存设置”按钮，注意：需要**重启**程序才能生效！！！"
        )
        self.save_setting = gr.Button("保存设置", variant="primary", size="lg")
        self.mainSetting()  # 主设置页面

        # 保存设置
        def warning():
            gr.Info("保存成功，下次重启程序生效！")

        self.save_setting.click(warning)

    def mainSetting(self):
        with gr.Tab(label="主设置"):
            # 显示设置
            if not os.path.exists(self.main_data_utils.main_setting.main_data_path):
                gr.Markdown(
                    "### 未找到设置文件，请重启程序。（重启程序会自动创建设置文件）"
                )
                return
            with open(
                self.main_data_utils.main_setting.main_data_path, "r", encoding="utf-8"
            ) as f:
                data = json.load(f)
            # 下面是可以设置的
            with gr.Row():
                temp_file_save_time_input = gr.Number(
                    label="临时文件保存时间(temp_file_save_time)",
                    info="如果设置为0，启动程序会自动清理所有临时文件",
                    maximum=100,
                    minimum=0,
                    step=1,
                    value=data.get(
                        "temp_file_save_time",
                        self.main_data_utils.main_setting.temp_file_save_time,
                    ),
                    interactive=True,
                )
                is_auto_clean_temp_input = gr.Checkbox(
                    label="是否自动清理临时文件",
                    info="is_auto_clean_temp",
                    value=data.get(
                        "is_auto_clean_temp",
                        self.main_data_utils.main_setting.is_auto_clean_temp,
                    ),
                    interactive=True,
                )
                max_prefix_length_input = gr.Number(
                    label="最大前缀字符长度",
                    info="max_prefix_length",
                    maximum=100,
                    minimum=1,
                    step=1,
                    value=data.get(
                        "max_prefix_length",
                        self.main_data_utils.main_setting.max_prefix_length,
                    ),
                    interactive=True,
                )
                auto_open_browser_input = gr.Checkbox(
                    label="是否自动打开浏览器",
                    info="auto_open_browser",
                    value=data.get(
                        "auto_open_browser",
                        self.main_data_utils.main_setting.auto_open_browser,
                    ),
                    interactive=True,
                )

            # 显示提示信息
            gr.Markdown("### 注意：下面这些设置会影响到程序的运行，我将其禁用了。")
            gr.Markdown(
                f"### 如果你有经验，请去：{self.main_data_utils.main_setting.main_data_path} 中修改。"
            )
            # api设置
            with gr.Row():
                api_host_input = gr.Textbox(
                    label="API的host",
                    info="api_host",
                    value=data.get(
                        "api_host", self.main_data_utils.main_setting.api_host
                    ),
                    interactive=False,
                )
                api_port_input = gr.Textbox(
                    label="API的端口",
                    info="api_port",
                    value=data.get(
                        "api_port", self.main_data_utils.main_setting.api_port
                    ),
                    interactive=False,
                )
            # api url 设置
            with gr.Row():
                api_url_character_list_input = gr.Textbox(
                    label="API的角色列表URL",
                    info="api_url_character_list",
                    value=data.get(
                        "api_url_character_list",
                        self.main_data_utils.main_setting.api_url_character_list,
                    ),
                    interactive=False,
                )
                api_url_txt_to_wav_input = gr.Textbox(
                    label="API的文本转语音URL",
                    info="api_url_txt_to_wav",
                    value=data.get(
                        "api_url_txt_to_wav",
                        self.main_data_utils.main_setting.api_url_txt_to_wav,
                    ),
                    interactive=False,
                )
            # app设置
            with gr.Row():
                app_local_host_input = gr.Textbox(
                    label="本地host",
                    info="app_local_host",
                    value=data.get(
                        "app_local_host",
                        self.main_data_utils.main_setting.app_local_host,
                    ),
                    interactive=False,
                )
                app_local_port_input = gr.Textbox(
                    label="本地端口",
                    info="app_local_port",
                    value=data.get(
                        "app_local_port",
                        self.main_data_utils.main_setting.app_local_port,
                    ),
                    interactive=False,
                )

        # 保存设置，保存主设置
        self.save_setting.click(
            self.saveMainSetting,
            inputs=[
                temp_file_save_time_input,
                is_auto_clean_temp_input,
                max_prefix_length_input,
                auto_open_browser_input,
            ],
        )

    def saveMainSetting(
        self,
        temp_file_save_time_input,
        is_auto_clean_temp_input,
        max_prefix_length_input,
        auto_open_browser_input,
    ):
        wait_save_data = {
            "temp_file_save_time": temp_file_save_time_input,
            "is_auto_clean_temp": True if is_auto_clean_temp_input else False,
            "max_prefix_length": max_prefix_length_input,
            "auto_open_browser": True if auto_open_browser_input else False,
        }
        self.main_data_utils.main_setting.update_data(wait_save_data)
