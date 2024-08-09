import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 获取和储存主要页面使用的数据
import asyncio
import datetime
import os
import random
import re
import time
import json
import requests

# 继承所有设置数据
from link_utils import LinkUtils
from metadata_wav import MetadataWav

# 在wav文件中添加元数据
metadata_wav = MetadataWav()


class MainData(LinkUtils):
    def __init__(self):
        super().__init__()
        self.main_setting  # 获取所有主页面设置的数据

    # 推理获取结果
    async def interface(self, model_name, txt, illation_num=5):
        all_data = self.get_all_data(model_name)
        # 生成推理结果
        random_results = self.random_generate(
            all_data, illation_num
        )  # 生成多个推理结果
        for selected_result in random_results:
            # 对每个推理结果发送请求并保存音频文件，收集所有文件的路径
            wav_file_path = self.post_txt(
                txt, model_name, selected_result
            )  # 发送请求，返回音频文件路径
            await asyncio.sleep(0.1)  # 等待0.1秒
            yield wav_file_path  # 返回音频文件路径

    # 获取文件名储存格式
    def get_filename(self, txt: str) -> str:
        # 获取当前时间戳
        timestamp = str(int(time.time()))
        # 如果txt是多行文本，合并为一行
        txt = txt.replace("\n", "_")
        txt = re.sub(r'[\\/:*?"<>|]', "_", txt)
        # 多余的字符用省略号代替
        if len(txt) > self.main_setting.max_prefix_length:
            # 文件名中加入时间戳，确保每次都不同
            return txt[: self.main_setting.max_prefix_length] + "..." + "+" + timestamp
        else:
            return txt + "+" + timestamp

    # 获取配置储存最后的模型
    def get_last_model(self, all_models):
        if os.path.exists(self.main_setting.last_model_path):
            with open(self.main_setting.last_model_path, "r", encoding="utf-8") as f:
                last_model = f.read()
            if last_model in all_models:
                return last_model
        return all_models[0]

    # 保存最后的模型
    def save_last_model(self, model_name):
        with open(self.main_setting.last_model_path, "w", encoding="utf-8") as f:
            f.write(model_name)

    # 获取推理次数结果
    def get_illation_num(self):
        if os.path.exists(self.main_setting.last_illation_num):
            with open(self.main_setting.last_illation_num, "r", encoding="utf-8") as f:
                illation_num = f.read()
            return int(illation_num) if illation_num.isdigit() else 5
        return 5

    # 保存推理次数结果
    def save_illation_num(self, illation_num):
        with open(self.main_setting.last_illation_num, "w", encoding="utf-8") as f:
            f.write(str(illation_num))

    # 获取测试文本
    def get_test_txt(self):
        if os.path.exists(self.main_setting.last_test_txt):
            with open(self.main_setting.last_test_txt, "r", encoding="utf-8") as f:
                test_txt = f.read()
            if test_txt.strip():
                return test_txt
        return "你好啊，我是你的智能语音助手"

    # 保存测试文本
    def save_test_txt(self, test_txt):
        if not test_txt.strip():
            test_txt = "你好啊，我是你的智能语音助手"
        with open(self.main_setting.last_test_txt, "w", encoding="utf-8") as f:
            f.write(test_txt)

    # 保存一个模型的所有数据
    def save_all_data(self, all_data):
        if not all_data or not all_data.get("model_name"):
            return
        model_name = all_data.get("model_name")
        model_path = os.path.join(
            self.main_setting.config_all_model_last_data_folder, f"{model_name}.json"
        )
        with open(model_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

    # 获取一个模型的所有数据
    def get_all_data(self, model_name):
        if not model_name:
            return {}
        model_path = os.path.join(
            self.main_setting.config_all_model_last_data_folder, f"{model_name}.json"
        )
        if os.path.exists(model_path):
            # 尝试次数
            try_count = 0
            while try_count < 3:
                try:
                    if os.path.getsize(model_path) == 0:  # 检查文件是否为空
                        return {}
                    with open(model_path, "r", encoding="utf-8") as f:
                        all_data = json.load(f)
                    return all_data
                except json.JSONDecodeError:
                    try_count += 1
                    time.sleep(0.5)
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

        # 生成随机推理结果
        results = []
        for _ in range(illation_num):  # 生成多个推理结果
            # 确保多次推理结果，每个情感都有机会被选中
            all_emotions = all_data.get("emotions")
            emotion = random.choice(all_emotions if all_emotions else ["default"])
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
        outputFilePath = os.path.join(
            self.main_setting.temp_folder, f"{self.get_filename(txt)}.wav"
        )
        # txt转url编码
        txt = requests.utils.quote(txt)
        # 获取输入的种子
        seed = random_dict["seed"]
        # 如果种子是-1，空字符串或者None，生成一个随机种子
        actual_seed = seed if seed not in [-1, "", None] else random.randrange(1 << 32)
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
            "seed": actual_seed,  # 随机种子
            "save_temp": random_dict[
                "save_temp"
            ],  # 是否保存临时文件，为true时，后端会保存生成的音频，下次相同请求会直接返回该数据，默认为false。
            "stream": random_dict[
                "stream"
            ],  # 是否流式传输，为true时，会按句返回音频，默认为false。
        }
        response = requests.post(self.main_setting.api_url_txt_to_wav, json=data)
        # 如果是错误信息，返回错误信息
        if response.status_code != 200:
            print(response.json())
            return
        # 保持wav文件
        with open(outputFilePath, "wb") as f:
            f.write(response.content)
        metadata_wav.add_metadata_to_wav(outputFilePath, data)  # 写入元数据
        return outputFilePath  # 返回文件路径

    # 自动清理临时文件
    def auto_clean_temp(self):
        if not self.main_setting.is_auto_clean_temp:
            return
        # 获取当前时间
        now = datetime.datetime.now()
        if self.temp_file_save_time < 0:
            self.temp_file_save_time = 7  # 默认保存7天
        # 计算过期时间
        expire_time = now - datetime.timedelta(days=self.temp_file_save_time)
        # 遍历临时文件夹
        for file_name in os.listdir(self.main_setting.temp_folder):
            # 获取文件的创建时间
            file_path = os.path.join(self.main_setting.temp_folder, file_name)
            create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            # 如果文件创建时间早于过期时间，删除文件
            if create_time <= expire_time:
                os.remove(file_path)
