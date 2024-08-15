import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gradio as gr
from tkinter import Tk, filedialog

# 继承所有设置数据
from settings import GSV_setting


class GSVUtils(GSV_setting.GSVSetting):
    def __init__(self):
        super().__init__()

    # 选择GPT-soVITS路径，并保存
    def select_GSV_Folder(self):
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        folder_path = filedialog.askdirectory()
        root.destroy()
        if folder_path:
            if self.save_GSV_path(folder_path):
                gr.Info(f"GPT-soVITS路径:“ {folder_path} ”保存成功!")
                pathone_path = self.check_GSV_python_embedded_path_get(folder_path)
                if pathone_path:
                    gr.Info(f"检测到Python环境文件夹:“ {pathone_path} ”，已使用！")
                return (str(folder_path), str(pathone_path))
            else:
                gr.Warning(f"GPT-soVITS路径:“ {folder_path} ”保存失败，请检查原因！")
        return (None, None)

    # 选择python环境路径，并保存
    def select_python_embedded_path(self):
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        folder_path = filedialog.askdirectory()
        root.destroy()
        if folder_path:
            if self.save_GSV_python_embedded_path(folder_path):
                gr.Info(f"Python环境:“ {folder_path} ”保存成功!")
                return str(folder_path)
            else:
                gr.Warning(f"Python环境:“ {folder_path} ”无法使用，请检查原因！")

        return None

    # 加载GSV路径和Python环境路径
    def reload_GSV_path_python(self):
        GSV_path_input = gr.update(value=self.get_GSV_path())
        GSV_python_embedded_path_input = gr.update(
            value=self.get_GSV_python_embedded_path()
        )
        return (GSV_path_input, GSV_python_embedded_path_input)

    # 加载api配置文件，并进行错误处理
    def load_api_config(self):
        api_config = self.get_GSV_api_config()
        # 对一些数据进行处理
        if not os.path.exists(api_config.get("api_file_path")):
            api_config["api_file_path"] = ""
        if not api_config.get("address"):
            api_config["address"] = "127.0.0.1"
        if not api_config.get("port"):
            api_config["port"] = 9880
        if api_config.get("device") not in ["cpu", "cuda", ""]:
            api_config["device"] = ""
        if api_config.get("precision") not in ["fp", "hp", ""]:
            api_config["precision"] = ""

        api_config["stream_mode"] = "close"
        api_config["media_type"] = "wav"

        if api_config.get("hubert_path") == None:
            api_config["hubert_path"] = ""
        if api_config.get("bert_path") == None:
            api_config["bert_path"] = ""
        if api_config != self.get_GSV_api_config():
            self.save_GSV_api_config(api_config)
        return api_config

    # 加载api配置文件
    def reload_GSV_api_data(self):
        api_data = self.load_api_config()
        GSV_api_file_path_input = gr.update(value=api_data["api_file_path"])
        GSV_address_input = gr.update(value=api_data["address"])
        GSV_port_input = gr.update(value=api_data["port"])
        GSV_device_input = gr.update(
            value=("使用默认" if api_data["device"] == "" else api_data["device"])
        )
        GSV_precision_input = gr.update(
            value=("使用默认" if api_data["precision"] == "" else api_data["precision"])
        )
        GSV_stream_mode_input = gr.update(value=api_data["stream_mode"])
        GSV_media_type_input = gr.update(value=api_data["media_type"])
        GSV_hubert_path_input = gr.update(value=api_data["hubert_path"])
        GSV_bert_path_input = gr.update(value=api_data["bert_path"])
        return (
            GSV_api_file_path_input,
            GSV_address_input,
            GSV_port_input,
            GSV_device_input,
            GSV_precision_input,
            GSV_stream_mode_input,
            GSV_media_type_input,
            GSV_hubert_path_input,
            GSV_bert_path_input,
        )

    # 加载模型列表
    def get_all_GSV_model(self) -> list:
        # 读取一个文件夹下的文件夹列表
        model_path = self.GSV_model_path
        if not os.path.exists(model_path):
            # 如果不存在，创建文件夹，多文件夹
            os.makedirs(model_path, exist_ok=True)
            return []
        # 读取文件夹
        return [
            _
            for _ in os.listdir(model_path)
            if os.path.isdir(os.path.join(model_path, _))
        ]

    # 加载GPT模型列表
    def reload_GPT_model_list(self, model_name, model_type="ckpt"):
        model_path = self.GSV_model_path
        if not os.path.exists(os.path.join(model_path, model_name)):
            os.makedirs(os.path.join(model_path, model_name), exist_ok=True)
            return []
        return [
            os.path.join(self.GSV_model_path, model_name, _)
            for _ in os.listdir(os.path.join(model_path, model_name))
            if _.endswith(model_type)
        ]

    # 加载SoVITS模型列表
    def reload_SoVITS_model_list(self, model_name):
        return self.reload_GPT_model_list(model_name, "pth")

    # 加载模型的参考音频列表
    def reload_model_audio_list(self, model_name):
        audio_extensions = [".wav", ".mp3", ".flac", ".aac", ".ogg", ".m4a", ".wma"]
        return self.reload_GPT_model_list(model_name, tuple(audio_extensions))

    # 在gr上显示所有模型
    def reload_gr_GSV_model(self):
        all_GSV_model_list = self.get_all_GSV_model()
        return gr.update(
            choices=all_GSV_model_list,
            value=all_GSV_model_list[0] if all_GSV_model_list else None,
        )

    # 加载所有模型数据
    def reload_GSV_model_audio(self, model_name):
        load_model_config = self.get_GSV_model_data(model_name)  # 加载模型配置

        all_GSV_model_list = self.reload_GPT_model_list(model_name)
        all_SoVITS_model_list = self.reload_SoVITS_model_list(model_name)
        all_audio_input_list = self.reload_model_audio_list(model_name)

        all_GSV_model = gr.update(
            choices=all_GSV_model_list if all_GSV_model_list else [],
            value=(
                load_model_config.get("GPT_model_path")
                if load_model_config and load_model_config.get("GPT_model_path")
                else all_GSV_model_list[0] if all_GSV_model_list else None
            ),
        )
        all_SoVITS_model = gr.update(
            choices=all_SoVITS_model_list if all_SoVITS_model_list else [],
            value=(
                load_model_config.get("SoVITS_model_path")
                if load_model_config and load_model_config.get("SoVITS_model_path")
                else all_SoVITS_model_list[0] if all_SoVITS_model_list else None
            ),
        )
        use_audio_data = (
            load_model_config.get("audio_data", {}) if load_model_config else {}
        )
        all_audio_emotion = []
        all_audio_input = []
        all_audio_text = []
        all_audio_language = []
        all_audio_preview = []
        for i in range(self.show_audio_num):
            if use_audio_data:
                use_emotion, use_dict = use_audio_data.popitem()
                if len(use_dict) == 3 and os.path.exists(use_dict[0]):
                    all_audio_emotion.append(
                        gr.update(
                            visible=True,
                            value=use_emotion,
                        )
                    )
                    all_audio_input.append(
                        gr.update(
                            visible=True,
                            value=use_dict[0],
                        )
                    )
                    if use_dict[0] in all_audio_input_list:
                        all_audio_input_list.remove(use_dict[0])
                    all_audio_text.append(
                        gr.update(
                            visible=True,
                            value=use_dict[1],
                        )
                    )
                    all_audio_language.append(
                        gr.update(
                            visible=True,
                            value=use_dict[2],
                        )
                    )
                    all_audio_preview.append(
                        gr.update(
                            visible=True,
                            value=use_dict[0],
                        )
                    )
                    continue
            if all_audio_input_list:
                all_audio_emotion.append(
                    gr.update(
                        visible=True,
                    )
                )
                audio_path = all_audio_input_list.pop(0)  # 弹出第一个
                all_audio_input.append(
                    gr.update(
                        visible=True,
                        value=audio_path,
                    )
                )
                all_audio_text.append(
                    gr.update(
                        visible=True,
                        value=os.path.splitext(os.path.basename(audio_path))[0],
                    )
                )
                all_audio_language.append(
                    gr.update(
                        visible=True,
                        value="多语种混合",
                    )
                )
                all_audio_preview.append(
                    gr.update(
                        visible=True,
                        value=audio_path,
                    )
                )
                continue
            for j in [
                all_audio_emotion,
                all_audio_input,
                all_audio_text,
                all_audio_language,
                all_audio_preview,
            ]:
                j.append(gr.update(visible=False))
        return (
            [all_GSV_model]
            + [all_SoVITS_model]
            + all_audio_emotion
            + all_audio_input
            + all_audio_text
            + all_audio_language
            + all_audio_preview
        )

    # 保存所有模型数据
    def save_all_GSV_model(
        self,
        model_name,
        GPT_model_path,
        SoVITS_model_path,
        *args,
    ):
        if not model_name or not GPT_model_path or not SoVITS_model_path or not args:
            return
        # 获取 self.show_audio_num 的值
        num = self.show_audio_num
        # 使用 self.show_audio_num 来切割 *args 中的数据
        all_audio_emotion = args[:num]
        all_audio_input = args[num : num * 2]
        all_audio_text = args[num * 2 : num * 3]
        all_audio_language = args[num * 3 : num * 4]

        if (
            not os.path.exists(os.path.join(self.GSV_model_path, model_name))
            or not os.path.exists(GPT_model_path)
            or not os.path.exists(SoVITS_model_path)
        ):
            return
        audio_data = {}

        for emotion, audio_input, audio_text, audio_language in zip(
            all_audio_emotion, all_audio_input, all_audio_text, all_audio_language
        ):
            if not emotion:
                continue
            if os.path.exists(audio_input):
                if not audio_text:
                    audio_text = os.splitext(os.path.basename(audio_input))[0]
                if not audio_language:
                    audio_language = "多语种混合"
                a = 1
                while emotion in audio_data:
                    emotion = emotion + str(a)
                    a += 1
                audio_data[emotion] = [audio_input, audio_text, audio_language]
        if self.save_model_data(
            model_name, GPT_model_path, SoVITS_model_path, audio_data
        ):
            gr.Info(f"模型:“ {model_name} ”保存成功！")
        else:
            gr.Warning(f"模型:“ {model_name} ”保存失败！")
