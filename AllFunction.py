import datetime
import os
import random
import re
import time
import json
import requests


# 这个是一个功能类，储存所有需要使用的功能函数
class AllFunction:
    # 配置文件路径
    def __init__(self):
        # 目标API的host和端口号
        self.host = "127.0.0.1"  # 目标API的host
        self.port = 5000  # 目标API的端口号
        self.url_character_list = (
            f"http://{self.host}:{self.port}/character_list"  # 获取所有模型的API
        )
        self.url_txt_to_wav = f"http://{self.host}:{self.port}/tts"  # 文本转语音的API

        # 本程序的host和端口号
        self.local_host = "127.0.0.1"  # 本程序的ip地址，默认为127.0.0.1
        self.local_port = 7861  # 本程序的端口号，默认为7860

        # 创建配置文件夹
        self.config_folder = "config"  # 配置文件夹
        self.check_folder(self.config_folder)  # 检查配置文件夹是否存在，不存在则创建

        # 临时文件夹
        self.temp_folder = "temp"  # 临时文件夹，用于保存wav文件
        self.check_folder(self.temp_folder)  # 临时文件夹，用于保存wav文件，不存在则创建
        self.temp_file_save_time = 7  # 临时文件保存时间，单位为天数（默认为7天），如果设置为0，立即清理所有临时文件
        self.is_auto_clean_temp = True  # 是否自动清理临时文件，True or False

        self.auto_clean_temp()  # 自动清理临时文件

        # 其他设置
        self.max_prefix_length = 30  # 保存文件名时，最大前缀字符长度
        self.auto_open_browser = True  # 是否自动打开浏览器，True or False

    # 获取文件名储存格式
    def get_filename(self, txt: str) -> str:
        # 获取当前时间戳
        timestamp = str(int(time.time()))
        # 如果txt是多行文本，合并为一行
        txt = txt.replace("\n", "_")
        txt = re.sub(r'[\\/:*?"<>|]', "_", txt)
        # 多余的字符用省略号代替
        if len(txt) > self.max_prefix_length:
            # 文件名中加入时间戳，确保每次都不同
            return txt[: self.max_prefix_length] + "..." + "+" + timestamp
        else:
            return txt + "+" + timestamp

    # 获取配置储存最后的模型
    def get_last_model(self, all_models):
        if os.path.exists(f"{self.config_folder}/last_model.txt"):
            with open(
                f"{self.config_folder}/last_model.txt", "r", encoding="utf-8"
            ) as f:
                last_model = f.read()
            if last_model in all_models:
                return last_model
        return all_models[0]

    # 保存最后的模型
    def save_last_model(self, model_name):
        with open(f"{self.config_folder}/last_model.txt", "w", encoding="utf-8") as f:
            f.write(model_name)

    # 获取推理次数结果
    def get_illation_num(self):
        if os.path.exists(f"{self.config_folder}/illation_num.txt"):
            with open(
                f"{self.config_folder}/illation_num.txt", "r", encoding="utf-8"
            ) as f:
                illation_num = f.read()
            return int(illation_num)
        return 5

    # 保存推理次数结果
    def save_illation_num(self, illation_num):
        with open(f"{self.config_folder}/illation_num.txt", "w", encoding="utf-8") as f:
            f.write(str(illation_num))

    # 获取测试文本
    def get_test_txt(self):
        if os.path.exists(f"{self.config_folder}/test_txt.txt"):
            with open(f"{self.config_folder}/test_txt.txt", "r", encoding="utf-8") as f:
                test_txt = f.read()
            return test_txt
        return "你好啊，我是你的智能语音助手"

    # 保存测试文本
    def save_test_txt(self, test_txt):
        with open(f"{self.config_folder}/test_txt.txt", "w", encoding="utf-8") as f:
            f.write(test_txt)

    # 保存一个模型的所有数据
    def save_all_data(self, all_data):
        if not all_data or not all_data.get("model_name"):
            return
        model_name = all_data.get("model_name")
        with open(
            f"{self.config_folder}/{model_name}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

    # 获取一个模型的所有数据
    def get_all_data(self, model_name):
        if not model_name:
            return {}
        if os.path.exists(f"{self.config_folder}/{model_name}.json"):
            with open(
                f"{self.config_folder}/{model_name}.json", "r", encoding="utf-8"
            ) as f:
                all_data = json.load(f)
            return all_data
        return {}

    # 随机生成推理结果
    def random_generate(self, all_data: dict, illation_num=5) -> list:
        def is_random_get_value(value_list: list, is_int: bool):  # 判断是否随机，返回值
            is_random = value_list[0]  # bool, 是否随机
            if is_random:
                min_value = min(value_list[2], value_list[3])
                max_value = max(value_list[2], value_list[3])
                return (
                    random.randint(min_value, max_value)
                    if is_int
                    else round(random.uniform(min_value, max_value), 2)
                )
            else:
                return value_list[1]

        # 切割方法转化
        def cut_method(cut_method: str):
            if cut_method in [
                "auto_cut",
                "cut0",
                "cut1",
                "cut2",
                "cut3",
                "cut4",
                "cut5",
            ]:
                return cut_method
            if cut_method == "智能切分":
                return "auto_cut"
            elif cut_method == "仅凭换行切分":
                return "cut0"
            elif cut_method == "凑四句一切":
                return "cut1"
            elif cut_method == "凑50字一切":
                return "cut2"
            elif cut_method == "按中文句号。切":
                return "cut3"
            elif cut_method == "按英文句号.切":
                return "cut4"
            elif cut_method == "按标点符号切":
                return "cut5"
            else:
                return "auto_cut"

        # 模拟的推理过程，实际应用中应替换为调用推理API
        results = []
        for _ in range(illation_num):  # 生成多个推理结果
            # 确保多次推理结果，每个情感都有机会被选中
            emotion = random.choice(all_data.get("emotions", ["default"]))
            top_k = is_random_get_value(all_data.get("top_k", [False, 5, 1, 10]), True)
            top_p = is_random_get_value(
                all_data.get("top_p", [False, 0.8, 0.7, 0.9]), False
            )
            temperature = is_random_get_value(
                all_data.get("temperature", [False, 0.8, 0.7, 0.9]), False
            )
            batch_size = is_random_get_value(
                all_data.get("batch_size", [False, 10, 5, 15]), True
            )
            max_cut_length = is_random_get_value(
                all_data.get("max_cut_length", [False, 50, 50, 50]), True
            )
            repetition_penalty = is_random_get_value(
                all_data.get("repetition_penalty", [False, 1.35, 1.35, 1.35]), False
            )

            result = {
                # 随机生成的参数
                "emotion": emotion,
                "batch_size": batch_size,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "max_cut_length": max_cut_length,
                "repetition_penalty": repetition_penalty,
                # 以下是不随机的参数
                "sample_rate": all_data.get("sample_rate", 32000),
                "speed": all_data.get("speed", 1.0),
                "save_temp": all_data.get("save_temp", "false"),
                "text_language": all_data.get("text_language", "auto"),
                "cut_method": cut_method(all_data.get("cut_method", "auto_cut")),
                "seed": all_data.get("seed", -1),
                "parallel_infer": all_data.get("parallel_infer", "true"),
                # 以下是不提供交互的参数
                "task_type": all_data.get("task_type", "text"),
                "format": all_data.get("format", "wav"),
                "stream": all_data.get("stream", "false"),
                "prompt_text": all_data.get("prompt_text", ""),
                "prompt_language": all_data.get("prompt_language", "auto"),
            }
            results.append(result)
        return results

    # 发送post请求
    def post_txt(self, txt, mode_name, random_dict):
        # 获取文件名，用于保存wav文件
        filename = (
            f"temp/{self.get_filename(txt)}.wav"  # 使用get_filename函数生成文件名
        )
        # txt转url编码
        txt = requests.utils.quote(txt)
        data = {
            "character": mode_name,
            "emotion": random_dict["emotion"],  # 情感
            "task_type": random_dict["task_type"],  # 任务类型，默认为text。
            "text": txt,
            "format": random_dict["format"],  # 保存格式，默认为wav。
            "text_language": random_dict[
                "text_language"
            ],  # 中文 、 英文 、 日文 、 中英混合 、 日英混合 、 多语种混合
            "prompt_text": random_dict["prompt_text"],  # 参考文本，不提供交互。
            "prompt_language": random_dict[
                "prompt_language"
            ],  # 参考文本的语言，应该也包含在情感列表中，默认为auto。
            "batch_size": random_dict["batch_size"],  # 批处理大小，整数，默认为10。
            "speed": random_dict["speed"],  # 语速，默认1.0。
            "top_k": random_dict["top_k"],
            "top_p": random_dict["top_p"],
            "temperature": random_dict["temperature"],
            "sample_rate": random_dict["sample_rate"],  # 采样率，默认32000。
            # 智能切分： auto_cut ， 仅凭换行切分： cut0 ， 凑四句一切： cut1
            # 凑50字一切： cut2 ， 按中文句号。切： cut3 ， 按英文句号.切： cut4 ， 按标点符号切： cut5
            "cut_method": random_dict["cut_method"],
            "max_cut_length": random_dict[
                "max_cut_length"
            ],  # 最大切分长度，整数，默认为50。
            "repetition_penalty": random_dict[
                "repetition_penalty"
            ],  # 重复惩罚，数值越大，越不容易重复，默认为1.35。
            "parallel_infer": random_dict[
                "parallel_infer"
            ],  # 是否并行推理，为true时，会加速很多，默认为true。
            "seed": random_dict["seed"],  # 随机种子，默认为-1。
            "save_temp": random_dict[
                "save_temp"
            ],  # 是否保存临时文件，为true时，后端会保存生成的音频，下次相同请求会直接返回该数据，默认为false。
            "stream": random_dict[
                "stream"
            ],  # 是否流式传输，为true时，会按句返回音频，默认为false。
        }
        response = requests.post(self.url_txt_to_wav, json=data)
        # 如果是错误信息，返回错误信息
        if response.status_code != 200:
            print(response.json())
            return
        # 保持wav文件
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename  # 返回文件路径

    # 自动清理临时文件
    def auto_clean_temp(self):
        if not self.is_auto_clean_temp:
            return
        # 获取当前时间
        now = datetime.datetime.now()
        if self.temp_file_save_time < 0:
            self.temp_file_save_time = 7  # 默认保存7天
        # 计算过期时间
        expire_time = now - datetime.timedelta(days=self.temp_file_save_time)
        # 遍历临时文件夹
        for file_name in os.listdir(self.temp_folder):
            # 获取文件的创建时间
            file_path = os.path.join(self.temp_folder, file_name)
            create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            # 如果文件创建时间早于过期时间，删除文件
            if create_time <= expire_time:
                os.remove(file_path)

    # 检查文件夹是否存在，不存在则创建
    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
