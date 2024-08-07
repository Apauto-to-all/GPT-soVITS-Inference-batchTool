# 主要页面的一些设置
import os
import sys

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config  # 导入文件名目录
from read_and_save import ReadAndSave

# 一个读取和保存数据的类
rs = ReadAndSave()


class MainSetting:
    def __init__(self) -> None:
        self.main_data_path = os.path.join(
            config.config_settings_folder, "main_data.json"
        )  # 主要数据的路径
        self.last_model_path = os.path.join(
            config.config_last_data_folder, "last_model.txt"
        )  # 最后使用的模型数据的路径
        self.last_illation_num = os.path.join(
            config.config_last_data_folder, "illation_num.txt"
        )  # 最后使用的迭代次数数据的路径
        self.last_test_txt = os.path.join(
            config.config_last_data_folder, "test_txt.txt"
        )  # 最后使用的测试文本数据的路径

        self.set_all_folder()  # 设置所有文件夹
        self.set_all_data()  # 设置所有数据

        # 读取情感列表
        self.all_models_emotions = self.get_model_emotions()
        self.all_models = (
            list(self.all_models_emotions.keys())
            if self.all_models_emotions != -1
            else []
        )

    # 获取感情列表
    def get_model_emotions(self) -> dict:
        # 读取情感列表
        try:
            response = requests.get(self.api_url_character_list)
            if response.status_code == 200:
                return response.json()  # 获取所有模型的情感列表
            else:
                return {}  # 或者抛出异常，或者返回错误信息
        except Exception as e:
            return -1

    def set_all_folder(self):
        self.config_all_model_last_data_folder = (
            config.config_all_model_last_data_folder
        )  # 所有模型最后使用的数据文件夹储存位置
        self.temp_folder = config.temp_folder  # 临时文件夹，用于保存wav文件

    def set_all_data(self):
        json_data = self.read_main_data()  # 读取主要数据
        self.set_api_data(json_data)  # 设置API数据
        self.set_app_data(json_data)  # 设置APP数据
        self.set_temp_data(json_data)  # 设置临时数据
        self.set_other_data(json_data)  # 设置其他数据

    def read_main_data(self):
        # 读取主要数据
        json_data = rs.read_json(self.main_data_path)
        if not json_data:
            self.recover_to_default()
            json_data = rs.read_json(self.main_data_path)
        return json_data

    def set_api_data(self, json_data):
        # 目标API的host和端口号
        self.api_host = json_data.get("api_host", "127.0.0.1")  # 目标API的host
        self.api_port = json_data.get("api_port", 5000)  # 目标API的端口号
        self.api_url_character_list = json_data.get(
            "api_url_character_list",
            f"http://{self.api_host}:{self.api_port}/character_list",
        )  # 获取所有模型的API
        self.api_url_txt_to_wav = json_data.get(
            "api_url_txt_to_wav", f"http://{self.api_host}:{self.api_port}/tts"
        )  # 文本转语音的API

    def set_app_data(self, json_data):
        # 本程序的host和端口号
        self.app_local_host = json_data.get(
            "app_local_host", "127.0.0.1"
        )  # 本程序的ip地址
        self.app_local_port = json_data.get("app_local_port", 7861)  # 本程序的端口号

    def set_temp_data(self, json_data):
        # 临时文件夹
        self.temp_file_save_time = json_data.get(
            "temp_file_save_time", 7
        )  # 临时文件保存时间，单位为天数（设置为0，立即清理所有临时文件）
        self.is_auto_clean_temp = json_data.get(
            "is_auto_clean_temp", True
        )  # 是否自动清理临时文件，True or False

    def set_other_data(self, json_data):
        # 其他设置
        self.max_prefix_length = json_data.get(
            "max_prefix_length", 30
        )  # 保存文件名时，最大前缀字符长度
        self.auto_open_browser = json_data.get(
            "auto_open_browser", True
        )  # 是否自动打开浏览器，True or False

    # 更新某一条数据
    def update_data(self, dict_data: dict):
        """
        更新多条数据
        : param dict_data: dict, 需要更新的数据，格式为{"key1": "value1", "key2": "value2", ...}
        """
        # 更新数据
        json_data = self.read_main_data()
        for key in dict_data:
            json_data[key] = dict_data[key]
        rs.save_json(self.main_data_path, json_data)

    # 文件缺失，恢复到初始设置
    def recover_to_default(self):
        """
        文件缺失，恢复到初始设置
        """
        api_host = "127.0.0.1"  # 目标API的host
        api_port = 5000  # 目标API的端口号
        api_url_character_list = (
            f"http://{api_host}:{api_port}/character_list"  # 获取所有模型的API
        )
        api_url_txt_to_wav = f"http://{api_host}:{api_port}/tts"  # 文本转语音的API

        # 本程序的host和端口号
        app_local_host = "127.0.0.1"  # 本程序的ip地址，默认为127.0.0.1
        app_local_port = 7861  # 本程序的端口号，默认为7860

        # 临时文件夹
        temp_file_save_time = (
            7  # 临时文件保存时间，单位为天数（设置为0，立即清理所有临时文件）
        )
        is_auto_clean_temp = True  # 是否自动清理临时文件，True or False

        # 其他设置
        max_prefix_length = 30  # 保存文件名时，最大前缀字符长度
        auto_open_browser = True  # 是否自动打开浏览器，True or False

        # 保持上面的设置
        data = {
            "api_host": api_host,  # 目标API的host
            "api_port": api_port,  # 目标API的端口号
            "api_url_character_list": api_url_character_list,  # 获取所有模型的API
            "api_url_txt_to_wav": api_url_txt_to_wav,  # 文本转语音的API
            "app_local_host": app_local_host,  # 本程序的ip地址
            "app_local_port": app_local_port,  # 本程序的端口号，默认为7860
            "temp_file_save_time": temp_file_save_time,  # 临时文件保存时间，单位为天数（设置为0，立即清理所有临时文件）
            "is_auto_clean_temp": is_auto_clean_temp,  # 是否自动清理临时文件，True or False
            "max_prefix_length": max_prefix_length,  # 保存文件名时，最大前缀字符长度
            "auto_open_browser": auto_open_browser,  # 是否自动打开浏览器，True or False
        }
        rs.save_json(self.main_data_path, data)
