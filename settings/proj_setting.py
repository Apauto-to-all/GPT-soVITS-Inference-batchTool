# 项目管理页面，储存一些项目的配置信息
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config  # 导入文件名目录
from read_and_save import ReadAndSave

# 一个读取和保存数据的类
rs = ReadAndSave()

# 一个项目配置
{
    "项目集合1": [
        "项目地址",
        ["子项目1", "子项目2"],
    ],
    "项目集合2": [
        "项目地址",
        ["子项目1", "子项目2"],
    ],
}


class ProjectSetting:
    def __init__(self):
        self.project_data_path = os.path.join(
            config.config_settings_folder, "project_data.json"
        )
        self.last_project_path = os.path.join(
            config.config_last_data_folder, "last_project.json"
        )

    # 获取项目集合数据
    def get_project_data(self) -> dict:
        """
        获取项目数据，完整数据，包括项目集合和子项目
        """
        data = rs.read_json(self.project_data_path)
        return data if data else {}

    # 获取所有项目集合名称
    def get_all_project_collection(self) -> list:
        """
        获取所有项目集合
        """
        all_data = self.get_project_data()
        return list(all_data.keys()) if all_data else []

    # 读取子项目数据
    def get_sub_project_data(self, project_collection_name) -> list:
        """
        获取子项目数据
        """
        data = self.get_project_data()
        return (
            data.get(project_collection_name, ["", []])[1]
            if project_collection_name in data
            else []
        )

    # 储存项目集合数据
    def save_project_data(self, project_data):
        """
        储存项目数据
        """
        rs.save_json(self.project_data_path, project_data)

    # 保存上次使用的项目
    def save_last_project(self, project_collection_name, sub_project_name):
        """
        保存上次使用的项目
        """
        if not project_collection_name or not sub_project_name:
            return
        rs.save_json(
            self.last_project_path,
            {project_collection_name: sub_project_name},
        )

    # 读取上次使用的项目，并检测是否可用
    def get_last_project(self):
        data = rs.read_json(self.last_project_path)  # {'项目集合': '子项目'}
        last_project_collection = list(data.keys())[0] if data else None
        last_sub_project = data.get(last_project_collection, None) if data else None
        all_project_collection = self.get_all_project_collection()
        if last_sub_project and last_project_collection:
            if last_project_collection in all_project_collection:
                all_sub_project = self.get_sub_project_data(last_project_collection)
                if last_sub_project in all_sub_project:
                    return data
        return {}

    # 获取上次使用的项目合集
    def get_last_project_collection(self):
        last_data = self.get_last_project()
        if last_data:
            return list(last_data.keys())[0]
        else:
            all_project_collection = self.get_all_project_collection()
            return all_project_collection[0] if all_project_collection else None

    # 获取上次使用的子项目
    def get_last_sub_project(self, project_collection=None):
        last_data = self.get_last_project()  # {'项目集合': '子项目'} 上次使用的项目
        if project_collection:
            last_project_collection = list(last_data.keys())[0] if last_data else None
            if project_collection == last_project_collection:
                return last_data.get(last_project_collection, None)
            else:
                all_sub_project = self.get_sub_project_data(project_collection)
                return all_sub_project[0] if all_sub_project else None
        else:
            return list(last_data.values())[0] if last_data else None
