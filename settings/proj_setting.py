# 项目管理页面，储存一些项目的配置信息
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

    # 检测项目集合和子项目是否存在
    def check_project_and_sub_project(
        self, project_collection_name, sub_project_name
    ) -> bool:
        """
        检测项目集合和子项目是否存在
        """
        if project_collection_name and sub_project_name:  # 如果项目集合和子项目都存在
            all_project_collection_list = self.get_all_project_collection()
            if (
                all_project_collection_list
                and project_collection_name in all_project_collection_list
            ):  # 如果项目集合存在，且在项目集合列表中
                all_sub_project_list = self.get_sub_project_data(
                    project_collection_name
                )
                if (
                    all_sub_project_list and sub_project_name in all_sub_project_list
                ):  # 如果子项目存在，且在子项目列表中
                    return True  # 返回True
        return False

    # 获取子项目路径
    def get_sub_project_path(self, project_collection_name, sub_project_name) -> str:
        """
        获取子项目路径
        """
        data = self.get_project_data()
        project_path = (
            data.get(project_collection_name, ["", []])[0]
            if project_collection_name in data
            else None
        )
        sub_project_path = os.path.join(project_path, sub_project_name)
        if os.path.exists(sub_project_path):
            return sub_project_path
        return None

    # 从上传使用的项目中获取项目路径
    def get_sub_project_path_from_last(self) -> str:
        """
        从上次使用的项目中获取项目路径
        """
        last_data = self.get_last_project()
        if last_data:
            project_collection_name = list(last_data.keys())[0]
            sub_project_name = last_data.get(project_collection_name)
            return self.get_sub_project_path(project_collection_name, sub_project_name)
        return None

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
        if self.check_project_and_sub_project(
            project_collection_name, sub_project_name
        ):
            rs.save_json(
                self.last_project_path,
                {project_collection_name: sub_project_name},
            )

    # 读取上次使用的项目，并检测是否可用
    def get_last_project(self):
        data = rs.read_json(self.last_project_path)  # {'项目集合': '子项目'}
        last_project_collection = list(data.keys())[0] if data else None  # 项目集合
        last_sub_project = (
            data.get(last_project_collection, None) if data else None
        )  # 子项目
        # 如果项目集合和子项目都存在
        if self.check_project_and_sub_project(
            last_project_collection, last_sub_project
        ):
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
        if project_collection:  # 如果提供项目集合
            last_project_collection = list(last_data.keys())[0] if last_data else None
            if project_collection == last_project_collection:
                return (
                    last_data.get(last_project_collection, None) if last_data else None
                )
            else:
                all_sub_project = self.get_sub_project_data(project_collection)
                return all_sub_project[0] if all_sub_project else None
        else:  # 如果没有提供项目集合
            return list(last_data.values())[0] if last_data else None
