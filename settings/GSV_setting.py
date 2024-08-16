# 适配GSV的api
import os
import re
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config  # 导入文件名目录

from read_and_save import ReadAndSave
from proj_setting import ProjectSetting
from main_setting import MainSetting

main_setting = MainSetting()

project_setting = ProjectSetting()

# 一个读取和保存数据的类
rs = ReadAndSave()

{
    "模型名称（文件夹名）": {
        "GPT_model_path": "GPT模型路径",
        "SoVITS_model_path": "SoVITS模型路径",
        "audio_data": {
            "情感1": [
                "音频1路径",
                "音频文本",
                "音频语言",
            ],
            "情感2": [
                "音频2路径",
                "音频文本",
                "音频语言",
            ],
        },
    },
    "模型名称1（文件夹名）": {...},
}


class GSVSetting:
    def __init__(self):
        # GSV_api设置
        self.GSV_api_config_path = os.path.join(
            config.config_settings_folder, "GSV_api_config.json"
        )
        # GSV文件夹路径
        self.GSV_path = os.path.join(config.config_last_data_GSV, "GSV_path.txt")
        # GSV的python嵌入式环境路径
        self.GSV_python_embedded_path = os.path.join(
            config.config_last_data_GSV, "GSV_python_embedded_path.json"
        )
        # GSV的model路径
        self.GSV_model_path = config.model_folder
        # GSV所有模型数据
        self.GSV_model_data_config_path = os.path.join(
            config.config_settings_folder, "GSV_model_data_config.json"
        )
        # 上一次使用的模型
        self.last_use_model = os.path.join(
            config.config_last_data_GSV, "last_model.txt"
        )
        # 上一次使用的推理文本，和推理次数
        self.last_use_text = os.path.join(config.config_last_data_GSV, "last_text.json")
        # 显示默认文件夹
        self.temp_folder = config.temp_folder
        # 显示音频数量
        self.show_audio_num = 10

    # 检测GPT-soVITS的文件夹
    def check_GSV_path(self, GSV_folder_path) -> bool:
        if not os.path.exists(GSV_folder_path):
            return False
        if not os.path.exists(os.path.join(GSV_folder_path, "api.py")):
            return False
        if not os.path.exists(os.path.join(GSV_folder_path, "GPT_SoVITS")):
            return False
        return True

    # 保存GSV文件夹路径
    def save_GSV_path(self, GSV_folder_path: str) -> bool:
        """
        保存GSV文件夹路径
        :param GSV_folder_path: GSV文件夹路径
        :return: 是否保存成功
        """
        if not self.check_GSV_path(GSV_folder_path):
            return False
        if rs.save_txt(
            self.GSV_path,
            GSV_folder_path,
        ):
            self.save_api_default_setting()
            return True

    # 获取GSV文件夹路径
    def get_GSV_path(self) -> str:
        return rs.read_txt(self.GSV_path)

    # 检测GPT-soVITS的文件夹下是否存在runtime文件夹（python嵌入式环境文件夹）
    def check_GSV_python_embedded_path_get(self, GSV_folder_path) -> str:
        """
        检测GPT-soVITS的文件夹下是否存在runtime文件夹（python嵌入式环境文件夹）
        :param GSV_folder_path: GPT-soVITS的文件夹
        :return: python嵌入式环境文件夹，没有则返回None
        """
        python_embedded_path = os.path.join(GSV_folder_path, "runtime")
        if self.save_GSV_python_embedded_path(python_embedded_path):
            return python_embedded_path
        return None

    # 检测python嵌入式环境文件夹，返回python版本
    def check_python_get_version(self, python_embedded_path) -> str:
        """
        检测python嵌入式环境文件夹，返回python版本
        :param python_embedded_path: python嵌入式环境文件夹
        :return: python版本，没有则返回None
        """
        if not os.path.exists(python_embedded_path):
            return None
        # 获取python版本
        try:
            python_version = (
                os.popen(f"{os.path.join(python_embedded_path, 'python')} --version")
                .read()
                .strip()
            )
            return python_version
        except Exception as e:
            return None

    # 保存GSV的python嵌入式环境路径
    def save_GSV_python_embedded_path(self, python_embedded_path: str) -> bool:
        """
        保存GSV文件夹路径
        :param GSV_folder_path: GSV文件夹路径
        :return: 是否保存成功
        """
        python_version = self.check_python_get_version(python_embedded_path)
        if not python_version:
            return False
        rs.save_json(
            self.GSV_python_embedded_path, [python_embedded_path, python_version]
        )
        return True

    # 获取GSV的python嵌入式环境版本
    def get_GSV_python_embedded_version(self) -> str:
        data = rs.read_json(self.GSV_python_embedded_path, [])
        if data and len(data) == 2:
            return data[1]
        return None

    # 获取GSV的python嵌入式环境python路径
    def get_GSV_python_embedded_python(self) -> str:
        python_path = self.get_GSV_python_embedded_path()
        if python_path:
            python_embedded_path = os.path.join(python_path, "python")
            return python_embedded_path
        return None

    # 获取GSV的python嵌入式环境路径
    def get_GSV_python_embedded_path(self) -> str:
        data = rs.read_json(self.GSV_python_embedded_path, [])
        if data and len(data) == 2:
            return data[0]
        return None

    # 保存默认设置
    def save_api_default_setting(self):
        # GSV文件夹路径
        GSV_path = rs.read_txt(self.GSV_path)
        if not self.check_GSV_path(GSV_path):
            return
        # api程序路径
        api_file_path = os.path.join(GSV_path, "api.py")
        # 设置api推理设备cuda or cpu（由GSV的api.py文件决定）
        device = ""
        # 设置api绑定地址
        address = "127.0.0.1"
        # 设置api绑定端口
        port = 9880
        # 选择半精度（hp）或全精度（fh），默认为半精度
        precision = ""  # fp / hp
        # 设置api流式返回模式，不启用
        stream_mode = "close"  # close / normal / keepalive
        # 设置返回的音频编码格式
        media_type = (
            ""  # 返回的音频编码格式, 流式默认ogg, 非流式默认wav, "wav", "ogg", "aac"
        )
        # 设置cnhubert路径
        hubert_path = ""
        # 设置bert路径
        bert_path = ""
        data = {
            "api_file_path": api_file_path,
            "device": device,
            "address": address,
            "port": port,
            "precision": precision,
            "stream_mode": stream_mode,
            "media_type": media_type,
            "hubert_path": hubert_path,
            "bert_path": bert_path,
        }
        rs.save_json(self.GSV_api_config_path, data)

    # 保存GSV的api配置
    def save_GSV_api_config(self, data: dict) -> bool:
        """
        保存GSV的api配置
        :param data: GSV的api配置
        :return: 是否保存成功
        """
        if not data:
            return False
        rs.save_json(self.GSV_api_config_path, data)
        return True

    # 获取GSV的API配置文件
    def get_GSV_api_config(self) -> dict:
        api_config = rs.read_json(self.GSV_api_config_path, {})
        if api_config:
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
            self.save_GSV_api_config(api_config)
            return api_config
        GSV_path = rs.read_txt(self.GSV_path)
        if GSV_path:
            self.save_api_default_setting()
            return rs.read_json(self.GSV_api_config_path, {})
        return {}

    # 检测模型所有数据是否正确
    def check_model_data(
        self, model_name, GPT_model_path, SoVITS_model_path, audio_data
    ):
        """
        检测模型所有数据是否正确
        :param model_name: 模型名称
        :param GPT_model_path: GPT模型路径
        :param SoVITS_model_path: SoVITS模型路径
        :param audio_data: 参考音频数据，格式为dict
        :return: 是否正确
        """
        if os.path.exists(os.path.join(self.GSV_model_path, model_name)):
            if os.path.exists(GPT_model_path) and os.path.exists(SoVITS_model_path):
                if audio_data:
                    for _, v in audio_data.items():
                        if len(v) == 3:
                            if not os.path.exists(v[0]):
                                return False
                    return True
        return False

    # 保存模型的所有数据
    def save_model_data(
        self, model_name, GPT_model_path, SoVITS_model_path, audio_data
    ) -> bool:
        """
        保存模型的所有数据
        :param model_name: 模型名称
        :param GPT_model_path: GPT模型路径
        :param SoVITS_model_path: SoVITS模型路径
        :param audio_data: 参考音频数据，格式为dict
        :return: 是否保存成功
        """
        if not self.check_model_data(
            model_name, GPT_model_path, SoVITS_model_path, audio_data
        ):
            return False
        model_data = {
            "GPT_model_path": GPT_model_path,
            "SoVITS_model_path": SoVITS_model_path,
            "audio_data": audio_data,
        }
        # 读取原有数据
        all_data = rs.read_json(self.GSV_model_data_config_path, {})
        if not all_data:
            all_data = {}
        all_data[model_name] = model_data
        rs.save_json(self.GSV_model_data_config_path, all_data)
        return True

    # 读取已经保存的模型的所有数据
    def get_GSV_model_data(self, model_name):
        all_model_data = rs.read_json(self.GSV_model_data_config_path, {})
        if all_model_data:
            return all_model_data.get(model_name, {})

    # 获取所有正在使用的模型
    def get_all_use_GSV_model_data(self) -> list:
        all_model = rs.read_json(self.GSV_model_data_config_path, {})
        return list(all_model.keys()) if all_model else []

    # 获取所有情感
    def get_all_emotion(self, model_name) -> list:
        all_model_data = rs.read_json(self.GSV_model_data_config_path, {})
        if all_model_data:
            model_data = all_model_data.get(model_name, {})
            return list(model_data.get("audio_data", {}).keys())
        return []

    # 获取上一次的模型
    def get_last_use_model(self) -> str:
        all_model_list = self.get_all_use_GSV_model_data()
        data = rs.read_json(self.last_use_model, [])
        if data and data in all_model_list:
            return data
        if all_model_list:
            self.save_last_model(all_model_list[0])
            return all_model_list[0]

    # 保存上一次使用的模型
    def save_last_model(self, model_name):
        all_model_list = self.get_all_use_GSV_model_data()
        if model_name in all_model_list:
            rs.save_txt(self.last_use_model, model_name)

    # 保持模型的推理参数
    def save_GSV_inference_setting(self, model_name: str, data: dict):
        """
        保持模型的推理参数
        :param model_name: 模型名称
        :param data: 推理参数
        :return: 是否保存成功
        """
        all_model_data = self.get_all_use_GSV_model_data()
        if all_model_data and model_name in all_model_data:
            rs.save_json(
                os.path.join(
                    config.config_all_model_last_data_GSV, f"{model_name}.json"
                ),
                data,
            )

    # 默认的推理参数
    def get_default_GSV_inference_setting(self, modle_name):
        data = {
            "model_name": modle_name,
            "emotions": [],
            "speed": 1.0,
            "top_k": [False, 15, 5, 20],
            "top_p": [False, 0.8, 0.7, 0.9],
            "temperature": [False, 0.8, 0.7, 0.9],
        }
        return data

    # 获取模型的推理参数
    def get_GSV_inference_setting(self, modle_name):
        modle_inference_setting_path = os.path.join(
            config.config_all_model_last_data_GSV, f"{modle_name}.json"
        )
        if os.path.exists(modle_inference_setting_path):
            return rs.read_json(modle_inference_setting_path, {})
        data = self.get_default_GSV_inference_setting(modle_name)
        self.save_GSV_inference_setting(modle_name, data)
        return data

    # 获取当前子路径
    def get_sub_project_path_from_last(self):
        return project_setting.get_sub_project_path_from_last()

    # 获取保存文件夹路径
    def get_last_save_text(self):
        data = rs.read_json(self.last_use_text, {})
        data["txt_input"] = data.get("txt_input", "你好啊，我是你的智能语音助手")
        data["text_language"] = data.get("text_language", "多语种混合")
        if data["text_language"] not in [
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
        ]:
            data["text_language"] = "多语种混合"
        data["cut_method_input"] = data.get("cut_method_input", "凑四句一切")
        if data["cut_method_input"] not in [
            "不切",
            "凑四句一切",
            "凑50字一切",
            "按中文句号。切",
            "按英文句号.切",
            "按标点符号切",
        ]:
            data["cut_method_input"] = "凑四句一切"
        data["illation_num_input"] = data.get("illation_num_input", 5)
        if (
            not isinstance(data["illation_num_input"], int)
            or data["illation_num_input"] < 1
            or data["illation_num_input"] > 20,
        ):
            data["illation_num_input"] = 5
        return data

    # 保存推理文本
    def save_last_save_text(
        self,
        txt_input,
        text_language,
        cut_method_input,
        illation_num_input,
    ):
        data = {
            "txt_input": txt_input,
            "text_language": text_language,
            "cut_method_input": cut_method_input,
            "illation_num_input": illation_num_input,
        }
        rs.save_json(self.last_use_text, data)

    # 获取情感的参考音频数据
    def get_emotion_data(self, model_name, emotion):
        model_data = self.get_GSV_model_data(model_name)
        if model_data:
            audio_data = model_data.get("audio_data", {})
            if emotion in audio_data and len(audio_data[emotion]) == 3:
                refer_wav_path = os.path.abspath(audio_data[emotion][0])
                prompt_text = audio_data[emotion][1]
                prompt_language = audio_data[emotion][2]
                return refer_wav_path, prompt_text, prompt_language
        return None, None, None

    # 获取文件名储存格式
    def get_filename(self, txt: str) -> str:
        # 获取当前时间戳
        timestamp = str(int(time.time()))
        # 如果txt是多行文本，合并为一行
        txt = txt.replace("\n", "_")
        txt = re.sub(r'[\\/:*?"<>|]', "_", txt)
        # 多余的字符用省略号代替
        if len(txt) > main_setting.max_prefix_length:
            # 文件名中加入时间戳，确保每次都不同
            return timestamp + "_" + txt[: main_setting.max_prefix_length] + "..."
        else:
            return timestamp + "_" + txt

    # 获取API的http地址
    def get_api_http_address(self):
        data = self.get_GSV_api_config()
        if data:
            return f"http://{data.get('address', '127.0.0.1')}:{data.get('port', 9880)}"
        else:
            return f"http://127.0.0.1:9880"
