# 项目管理工具，用于展示项目的文件
import json
import os
import sys
import gradio as gr
from tkinter import Tk, filedialog

# 将项目根目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from link_pages import LinkPages


class ProjPage(LinkPages):
    def __init__(self):
        super().__init__()

    # 在顶部选择项目
    def showSelectProj(self, demo: gr.Blocks):
        with gr.Row():
            self.use_project_collection = gr.Dropdown(
                label="项目集合",
                interactive=True,
            )
            self.use_sub_project = gr.Dropdown(
                label="子项目",
                interactive=True,
            )
            # 打开项目文件夹的按钮
            open_folder_btn = gr.Button("打开项目文件夹", variant="primary", size="sm")

        def open_sub_project_folder(project_collection, sub_project):
            if not project_collection or not sub_project:
                gr.Warning("项目集合和子项目不能为空")
                return
            sub_project_path = self.proj_mgmt_utils.proj_setting.get_sub_project_path(
                project_collection, sub_project
            )
            if not sub_project_path:
                gr.Warning(f"项目路径不存在，请检查")
                return
            if not os.path.exists(sub_project_path) and not os.path.isdir(
                sub_project_path
            ):
                gr.Warning(f"子项目路径： {sub_project_path} 不存在")
                return
            try:
                os.system(f"start {sub_project_path} ")
                gr.Info(f"项目文件夹已打开，注意查看！", duration=2)
            except Exception as e:
                gr.Warning(f"无法打开文件夹： {e}")

        open_folder_btn.click(
            open_sub_project_folder,
            inputs=[self.use_project_collection, self.use_sub_project],
        )

        def update_sub_project(collection):
            sub_project_up = gr.update(
                choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                    collection
                ),
                value=self.proj_mgmt_utils.proj_setting.get_last_sub_project(
                    collection
                ),
            )
            return sub_project_up

        self.use_project_collection.change(
            update_sub_project,
            inputs=[self.use_project_collection],
            outputs=[self.use_sub_project],
        )

        for change_project in [self.use_project_collection, self.use_sub_project]:
            change_project.change(
                self.proj_mgmt_utils.proj_setting.save_last_project,
                inputs=[self.use_project_collection, self.use_sub_project],
            )

        def update_last_use():
            return (
                gr.update(
                    choices=self.proj_mgmt_utils.proj_setting.get_all_project_collection(),
                    value=self.proj_mgmt_utils.proj_setting.get_last_project_collection(),
                ),
                gr.update(
                    choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                        self.proj_mgmt_utils.proj_setting.get_last_project_collection()
                    ),
                    value=self.proj_mgmt_utils.proj_setting.get_last_sub_project(),
                ),
            )

        demo.load(
            update_last_use,
            outputs=[self.use_project_collection, self.use_sub_project],
        )

    # 定义一个函数来处理文件夹选择
    def selectFolder(self):
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        folder_path = filedialog.askdirectory()
        root.destroy()
        if folder_path:
            return str(folder_path)
        else:
            return None

    # 使用gradio展示项目管理工具
    def showProjMgmt(self, demo: gr.Blocks):
        # 创建一个文件夹选择器
        with gr.Tab(label="项目管理"):
            # 创建一个新的项目集合
            gr.Markdown("### 创建一个新的项目集合")
            with gr.Row():
                project_collection_input_new_name = gr.Textbox(
                    label="项目集合名称",
                    placeholder="输入一个新的不重复的项目集合名称",
                    interactive=True,
                )
                project_collection_input_path = gr.Textbox(
                    label="项目集合路径",
                    placeholder="点击按钮获取文件夹",
                    interactive=False,
                )
                browse_btn = gr.Button("选择文件夹", variant="primary", size="sm")
                browse_btn.click(
                    self.selectFolder,
                    outputs=project_collection_input_path,
                    show_progress="hidden",
                )
                create_btn = gr.Button("创建项目集合", variant="primary", size="sm")

            # 创建一个新的子项目
            gr.Markdown("### 创建一个新的子项目")
            with gr.Row():
                project_collection_input_name = gr.Dropdown(
                    label="项目集合名称",
                    interactive=True,
                )
                sub_project_input_new_name = gr.Textbox(
                    label="子项目名称",
                    placeholder="输入一个新的不重复的子项目名称",
                    interactive=True,
                )
                create_sub_btn = gr.Button("创建子项目", variant="primary", size="sm")

            # 删除项目集合
            gr.Markdown("### 删除项目集合")
            with gr.Row():
                delete_project_collection = gr.Dropdown(
                    label="项目集合名称",
                    interactive=True,
                )
                delete_btn = gr.Button("删除项目集合", variant="stop", size="sm")

            # 删除子项目
            gr.Markdown("### 删除子项目")
            with gr.Row():
                delete_sub_project_project_collection = gr.Dropdown(
                    label="项目集合名称",
                    interactive=True,
                )
                delete_sub_project = gr.Dropdown(
                    label="子项目名称",
                    interactive=True,
                )
                delete_sub_btn = gr.Button("删除子项目", variant="stop", size="sm")

                def update_sub_project(collection):
                    sub_project_up = gr.update(
                        choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                            collection
                        ),
                        value=None,
                    )
                    return sub_project_up

                delete_sub_project_project_collection.change(
                    update_sub_project,
                    inputs=[delete_sub_project_project_collection],
                    outputs=[delete_sub_project],
                )

            # 所有需要更新的项目集合
            all_project_collection = [
                self.use_project_collection,
                project_collection_input_name,
                delete_project_collection,
                delete_sub_project_project_collection,
            ]

            # 自动加载项目集合
            def load_project_collection():
                return tuple(
                    gr.update(
                        choices=self.proj_mgmt_utils.proj_setting.get_all_project_collection(),
                    )
                    for _ in all_project_collection[1:]
                )

            demo.load(
                load_project_collection,
                outputs=all_project_collection[1:],
            )

            # 创建项目集合，然后更新项目集合内容
            def create_project_collection_up_project_collection(input_name, input_path):
                if not input_name or not input_path:
                    gr.Warning("项目集合名称和路径不能为空")
                    result = tuple(gr.update() for _ in all_project_collection)
                    return result
                message = self.proj_mgmt_utils.create_project_collection(
                    input_name, input_path
                )
                if message.get("error"):
                    gr.Warning(message["error"])
                else:
                    gr.Info(json.dumps(message, ensure_ascii=False))
                new_project_collection = gr.update(
                    choices=self.proj_mgmt_utils.proj_setting.get_all_project_collection(),
                )
                result = tuple(new_project_collection for _ in all_project_collection)
                return result

            # 绑定创建项目集合的按钮
            create_btn.click(
                create_project_collection_up_project_collection,
                inputs=[
                    project_collection_input_new_name,
                    project_collection_input_path,
                ],
                outputs=all_project_collection,
            )

            # 创建子项目，然后更新子项目内容
            def create_sub_project_up_sub_project(
                project_collection_name,
                sub_project_name,
                use_project_collection,
                delete_sub_project_project_collection,
            ):
                if not project_collection_name or not sub_project_name:
                    gr.Warning("项目集合名称和子项目名称不能为空")
                    return (gr.update(), gr.update())
                message = self.proj_mgmt_utils.create_sub_project(
                    project_collection_name, sub_project_name
                )
                if message.get("error"):
                    gr.Warning(message["error"])
                else:
                    gr.Info(json.dumps(message, ensure_ascii=False))
                use_project_collection_up = (
                    gr.update(
                        choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                            project_collection_name
                        )
                    )
                    if project_collection_name == use_project_collection
                    else gr.update()
                )
                delete_sub_project_project_collection_up = (
                    gr.update(
                        choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                            project_collection_name
                        )
                    )
                    if project_collection_name == delete_sub_project_project_collection
                    else gr.update()
                )
                return (
                    use_project_collection_up,
                    delete_sub_project_project_collection_up,
                )

            create_sub_btn.click(
                create_sub_project_up_sub_project,
                inputs=[
                    project_collection_input_name,
                    sub_project_input_new_name,
                    self.use_project_collection,
                    delete_sub_project_project_collection,
                ],
                outputs=[self.use_sub_project, delete_sub_project],
            )

            # 删除项目集合，然后更新项目集合内容
            def delete_project_collection_up_project_collection(collection):
                if not collection:
                    result = tuple(gr.update() for _ in all_project_collection)
                    return result
                message = self.proj_mgmt_utils.delete_project_collection(collection)
                if message.get("error"):
                    gr.Warning(message["error"])
                else:
                    gr.Info(json.dumps(message, ensure_ascii=False))
                new_project_collection = gr.update(
                    choices=self.proj_mgmt_utils.proj_setting.get_all_project_collection(),
                )
                result = tuple(new_project_collection for _ in all_project_collection)
                return result

            delete_btn.click(
                delete_project_collection_up_project_collection,
                inputs=[delete_project_collection],
                outputs=all_project_collection,
            )

            # 删除子项目，然后更新子项目内容
            def delete_sub_project_up_sub_project(
                delete_sub_project_project_collection,
                delete_sub_project,
                use_project_collection,
                use_sub_project,
            ):
                if not delete_sub_project_project_collection or not delete_sub_project:
                    gr.Warning("项目集合名称和子项目名称不能为空")
                    return (gr.update(), gr.update())
                if (
                    use_project_collection == delete_sub_project_project_collection
                    and use_sub_project == delete_sub_project
                ):
                    gr.Warning(
                        f"{use_project_collection} -- {use_sub_project} ：正在使用中，无法删除，请先更换子项目 “ {use_sub_project} ” "
                    )
                    return (gr.update(), gr.update())
                message = self.proj_mgmt_utils.delete_sub_project(
                    delete_sub_project_project_collection, delete_sub_project
                )
                if message.get("error"):
                    gr.Warning(message["error"])
                else:
                    gr.Info(json.dumps(message, ensure_ascii=False))
                new_sub_project = gr.update(
                    choices=self.proj_mgmt_utils.proj_setting.get_sub_project_data(
                        delete_sub_project_project_collection
                    )
                )
                use_project_collection_up = (
                    new_sub_project
                    if use_project_collection == delete_sub_project_project_collection
                    else gr.update()
                )
                return (use_project_collection_up, new_sub_project)

            delete_sub_btn.click(
                delete_sub_project_up_sub_project,
                inputs=[
                    delete_sub_project_project_collection,
                    delete_sub_project,
                    self.use_project_collection,
                    self.use_sub_project,
                ],
                outputs=[self.use_sub_project, delete_sub_project],
            )
