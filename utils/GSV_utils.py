import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import datetime
import random
import re
import time
import json
import requests
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

    # 加载api配置文件
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
