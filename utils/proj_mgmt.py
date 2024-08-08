import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 获取和储存主要页面使用的数据

# 继承所有设置数据
from link_utils import LinkUtils


class ProjectManagement(LinkUtils):
    def __init__(self):
        super().__init__()
        self.proj_setting

    # 创建项目集合
    def create_project_collection(self, project_collection_name, project_path):
        try:
            data = self.proj_setting.get_project_data()
            if project_collection_name in data:
                return {"error": "项目集合已存在"}
            if not os.path.exists(project_path) or not os.path.isdir(project_path):
                return {"error": "文件夹不存在"}
            # 检测文件路径是否重复
            for value in data.values():
                if project_path == value[0]:
                    return {"error": "该文件夹已使用"}
            data[project_collection_name] = [project_path, []]
            self.proj_setting.save_project_data(data)
            return {"success": "创建成功"}
        except Exception as e:
            return {"error": str(e)}

    # 创建子项目
    def create_sub_project(self, project_collection_name, sub_project_name):
        try:
            data = self.proj_setting.get_project_data()
            sub_project_path = os.path.join(
                data[project_collection_name][0], sub_project_name
            )
            if sub_project_name in data[project_collection_name][1]:
                return {"error": f"{sub_project_name} 子项目已存在"}

            # 如果文件夹不存在，就创建文件夹
            if not os.path.exists(sub_project_path):
                os.makedirs(sub_project_path)
            # 添加到子项目中
            data[project_collection_name][1].append(sub_project_name)
            # 保存数据
            self.proj_setting.save_project_data(data)
            return {"success": "创建成功"}
        except Exception as e:
            return {"error": str(e)}

    # 删除项目集合
    def delete_project_collection(self, project_collection_name):
        try:
            data = self.proj_setting.get_project_data()
            if project_collection_name not in data:
                return {"error": "项目集合不存在"}
            del data[project_collection_name]
            self.proj_setting.save_project_data(data)
            return {
                "success": "删除成功，本程序不会删除本地文件夹，如有需要，请手动删除"
            }
        except Exception as e:
            return {"error": str(e)}

    # 删除子项目
    def delete_sub_project(self, project_collection_name, sub_project_name):
        try:
            data = self.proj_setting.get_project_data()
            if sub_project_name not in data[project_collection_name][1]:
                return {"error": "子项目不存在"}
            data[project_collection_name][1].remove(sub_project_name)
            self.proj_setting.save_project_data(data)
            return {
                "success": "删除成功，本程序不会删除本地文件夹，如有需要，请手动删除"
            }
        except Exception as e:
            return {"error": str(e)}
