# 项目文件夹的文件夹信息
import os


# 检查文件夹是否存在，不存在则创建
def check_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# 配置文件夹
config_folder = "config"  # 配置文件夹
check_folder(config_folder)

# 配置设置文件夹
config_settings_folder = os.path.join(
    config_folder, "settings"
)  # 配置设置文件夹储存位置
check_folder(config_settings_folder)

# 配置最后使用的数据文件夹
config_last_data_folder = os.path.join(
    config_folder, "last_data"
)  # 配置最后使用的数据文件夹储存位置
check_folder(config_last_data_folder)

# 配置所有模型最后使用的数据
config_all_model_last_data_folder = os.path.join(
    config_folder, "all_model_last_data"
)  # 配置所有模型最后使用的数据文件夹储存位置
check_folder(config_all_model_last_data_folder)

# 临时文件夹
temp_folder = "temp"  # 临时文件夹，用于保存wav文件
check_folder(temp_folder)
