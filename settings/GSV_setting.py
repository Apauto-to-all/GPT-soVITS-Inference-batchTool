# 适配GSV的api
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config  # 导入文件名目录

from read_and_save import ReadAndSave

# 一个读取和保存数据的类
rs = ReadAndSave()

"""
## 执行参数:

`-s` - `SoVITS模型路径, 可在 config.py 中指定`
`-g` - `GPT模型路径, 可在 config.py 中指定`

调用请求缺少参考音频时使用
`-dr` - `默认参考音频路径`
`-dt` - `默认参考音频文本`
`-dl` - `默认参考音频语种, "中文","英文","日文","韩文","粤语,"zh","en","ja","ko","yue"`

`-d` - `推理设备, "cuda","cpu"`
`-a` - `绑定地址, 默认"127.0.0.1"`
`-p` - `绑定端口, 默认9880, 可在 config.py 中指定`
`-fp` - `覆盖 config.py 使用全精度`
`-hp` - `覆盖 config.py 使用半精度`
`-sm` - `流式返回模式, 默认不启用, "close","c", "normal","n", "keepalive","k"`
·-mt` - `返回的音频编码格式, 流式默认ogg, 非流式默认wav, "wav", "ogg", "aac"`
·-cp` - `文本切分符号设定, 默认为空, 以",.，。"字符串的方式传入`

`-hb` - `cnhubert路径`
`-b` - `bert路径`
dict_language = {
    "中文": "all_zh",
    "粤语": "all_yue",
    "英文": "en",
    "日文": "all_ja",
    "韩文": "all_ko",
    "中英混合": "zh",
    "粤英混合": "yue",
    "日英混合": "ja",
    "韩英混合": "ko",
    "多语种混合": "auto",    #多语种启动切分识别语种
    "多语种混合(粤语)": "auto_yue",
    "all_zh": "all_zh",
    "all_yue": "all_yue",
    "en": "en",
    "all_ja": "all_ja",
    "all_ko": "all_ko",
    "zh": "zh",
    "yue": "yue",
    "ja": "ja",
    "ko": "ko",
    "auto": "auto",
    "auto_yue": "auto_yue",
}

# logger
logging.config.dictConfig(uvicorn.config.LOGGING_CONFIG)
logger = logging.getLogger('uvicorn')

# 获取配置
g_config = global_config.Config()

# 获取参数
parser = argparse.ArgumentParser(description="GPT-SoVITS api")

parser.add_argument("-s", "--sovits_path", type=str, default=g_config.sovits_path, help="SoVITS模型路径")
parser.add_argument("-g", "--gpt_path", type=str, default=g_config.gpt_path, help="GPT模型路径")
parser.add_argument("-dr", "--default_refer_path", type=str, default="", help="默认参考音频路径")
parser.add_argument("-dt", "--default_refer_text", type=str, default="", help="默认参考音频文本")
parser.add_argument("-dl", "--default_refer_language", type=str, default="", help="默认参考音频语种")
parser.add_argument("-d", "--device", type=str, default=g_config.infer_device, help="cuda / cpu")
parser.add_argument("-a", "--bind_addr", type=str, default="0.0.0.0", help="default: 0.0.0.0")
parser.add_argument("-p", "--port", type=int, default=g_config.api_port, help="default: 9880")
parser.add_argument("-fp", "--full_precision", action="store_true", default=False, help="覆盖config.is_half为False, 使用全精度")
parser.add_argument("-hp", "--half_precision", action="store_true", default=False, help="覆盖config.is_half为True, 使用半精度")
# bool值的用法为 `python ./api.py -fp ...`
# 此时 full_precision==True, half_precision==False
parser.add_argument("-sm", "--stream_mode", type=str, default="close", help="流式返回模式, close / normal / keepalive")
parser.add_argument("-mt", "--media_type", type=str, default="wav", help="音频编码格式, wav / ogg / aac")
parser.add_argument("-cp", "--cut_punc", type=str, default="", help="文本切分符号设定, 符号范围,.;?!、，。？！；：…")
# 切割常用分句符为 `python ./api.py -cp ".?!。？！"`
parser.add_argument("-hb", "--hubert_path", type=str, default=g_config.cnhubert_path, help="覆盖config.cnhubert_path")
parser.add_argument("-b", "--bert_path", type=str, default=g_config.bert_path, help="覆盖config.bert_path")
"""


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
        data = rs.read_json(self.GSV_python_embedded_path)
        if data and len(data) == 2:
            return data[1]
        return None

    # 获取GSV的python嵌入式环境python路径
    def get_GSV_python_embedded_python(self) -> str:
        data = rs.read_json(self.GSV_python_embedded_path)
        if data and len(data) == 2:
            python_embedded_path = os.path.join(data[0], "python")
            return python_embedded_path
        return None

    # 获取GSV的python嵌入式环境路径
    def get_GSV_python_embedded_path(self) -> str:
        data = rs.read_json(self.GSV_python_embedded_path)
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

    # 获取GSV配置文件
    def get_GSV_api_config(self) -> dict:
        data = rs.read_json(self.GSV_api_config_path)
        if data:
            return data
        GSV_path = rs.read_txt(self.GSV_path)
        if GSV_path:
            self.save_api_default_setting()
            return rs.read_json(self.GSV_api_config_path)
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
        all_data = rs.read_json(self.GSV_model_data_config_path)
        if not all_data:
            all_data = {}
        all_data[model_name] = model_data
        rs.save_json(self.GSV_model_data_config_path, all_data)
        return True

    # 读取目标模型的所有数据
    def get_GSV_model_data(self, model_name):
        all_model_data = rs.read_json(self.GSV_model_data_config_path)
        if all_model_data:
            return all_model_data.get(model_name, {})


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
