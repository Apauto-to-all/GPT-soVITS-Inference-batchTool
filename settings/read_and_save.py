# 获取数据和保持数据的类
import json
import os


class ReadAndSave:
    def __init__(self):
        pass

    # 检查文件是否存在
    def check_file(self, file_path):
        if os.path.exists(file_path):
            return True
        return False

    # 读取json文件
    def read_json(self, file_path, default_type={}):
        """
        读取json文件
        :param file_path: 文件路径
        :return: 返回读取的数据
        """
        if not self.check_file(file_path):
            return default_type
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return default_type

    # 保存json文件
    def save_json(self, file_path, data):
        """
        保存json文件
        :param file_path: 文件路径
        :param data: 要保存的数据
        :return: 是否保存成功
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            return

    # 读取txt文件
    def read_txt(self, file_path) -> str:
        """
        读取txt文件
        :param file_path: 文件路径
        :return: 返回读取的数据
        """
        if not self.check_file(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(e)
            return None

    # 保存txt文件
    def save_txt(self, file_path, data):
        """
        保存txt文件
        :param file_path: 文件路径
        :param data: 要保存的数据
        :return: 是否保存成功
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            print(e)
            return False
        return True
