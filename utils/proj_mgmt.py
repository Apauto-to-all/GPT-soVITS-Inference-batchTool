# 项目管理工具，用于展示项目的文件
import os
import sys
import gradio as gr
from tkinter import Tk, filedialog

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as config


# 定义一个函数来处理文件夹选择
def select_folder():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    if folder_path:
        return str(folder_path)
    else:
        return "无文件夹"


# 使用gradio展示项目管理工具
def show_proj_mgmt():
    # 创建一个文件夹选择器
    with gr.Blocks() as demo:
        with gr.Row():
            input_path = gr.Textbox(
                label="项目储存目录", interactive=False, autoscroll=False
            )
            browse_btn = gr.Button("选择文件夹", variant="primary", size="sm")
            browse_btn.click(
                select_folder, inputs=None, outputs=input_path, show_progress="hidden"
            )

    # 启动接口
    demo.launch(inbrowser=True)


# 调用函数展示项目管理工具
show_proj_mgmt()
