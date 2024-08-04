# GPT-soVITS-Inference批量抽卡工具

- [GPT-soVITS-Inference批量抽卡工具](#gpt-sovits-inference批量抽卡工具)
  - [使用方法](#使用方法)
    - [克隆项目](#克隆项目)
    - [安装依赖](#安装依赖)
    - [运行](#运行)
  - [简单介绍用法](#简单介绍用法)
    - [一个是设置页面](#一个是设置页面)
    - [另一个是抽卡页面](#另一个是抽卡页面)
    - [下载保存的音频文件格式](#下载保存的音频文件格式)
  - [页面示例](#页面示例)
  - [许可证](#许可证)
  - [常见问题（FAQ）](#常见问题faq)
  - [后续计划](#后续计划)

这是一个批量推理工具，对同一段文字进行多次推理，并且支持随机参数，直到筛选出最满意的结果

显然，手动点击的方式不够高效，这个工具就是为了解决这个问题而设计的

适用于GPT-soVITS-Inference第三方推理包，GPT-soVITS-Inference基于GPT-soVITS开发的，专注于推理的前后端语音合成项目

> GPT-soVITS : [项目地址](https://github.com/RVC-Boss/GPT-SoVITS) , [中文指南](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e)
>
> GPT-soVITS-Inference : [项目地址](https://github.com/X-T-E-R/GPT-SoVITS-Inference) , [中文指南](https://www.yuque.com/xter/zibxlp)
>
> GPT-soVITS-Inference提供了比较简单的API接口，文档也较为完善，API接口文档可以在[这里](https://www.yuque.com/xter/zibxlp/knu8p82lb5ipufqy)查看

## 使用方法

### 克隆项目

```shell
git clone https://github.com/Apauto-to-all/GPT-soVITS-Inference-batchTool.git
```

### 安装依赖

本项目主要使用了 `gradio==4.39.0` 包和 `requests` 包，可以通过以下命令安装

```shell
pip install -r requirements.txt
```

使用国内源：

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行

首先需要**启动GPT-soVITS-Inference的后端服务**，然后运行`main.py`，否则程序无法正常运行

## 简单介绍用法

一共2个页面：

### 一个是设置页面

用来选择模型，选择使用的情感，设置一些推理用的参数，一些参数支持随机生成

### 另一个是抽卡页面

输入需要推理的文本

最高支持20连抽（应该够用，不够后续扩展）

点击抽卡按钮，程序使用前面设置的参数生成多个（随机）结果

发送到API接口，进行推理，每推理一次，在页面上显示一条音频结果，直到全部结果推理完毕

如果都不满意，可以再次点击抽卡按钮，重新推理

如果不希望再次推理，可以点击`停止`按钮，停止继续推理

如果有满意的结果，可以选择下载

### 下载保存的音频文件格式

由于`GPT-soVITS`和`GPT-soVITS-Inference`的推理下载的音频都是以`audio.wav`的形式返回的，难以区分，所以本项目在下载音频时，会将推理的文字的前30个字符作为文件名的一部分，加上时间戳，以区分不同的音频文件

下载的音频的文件名为`[推理文字的前30个字符]……+[时间戳].wav`，例如`这是一个测试……+1631234567.wav`

## 页面示例

- 设置页面

![alt text](/show/image.png)

- 抽卡页面

![alt text](/show/image-1.png)

## 许可证

本程序遵循 [MIT 许可证](https://opensource.org/license/mit/)。

更多关于 MIT 许可证的详细信息，请访问 [MIT 开源许可证](https://opensource.org/license/mit/) 的官方网站。

## 常见问题（FAQ）

- API地址默认使用`5000`端口，如果有需要，请在[`AllFunction.py`](AllFunction.py)文件中修改`self.port`变量的值

- 本项目默认部署在本地，使用`7861`端口，有需要也可以在[`AllFunction.py`](AllFunction.py)文件找到相应的变量进行修改

- 所有音频文件都会保存在`temp`文件夹下，文件默认保存7天，可以在[`AllFunction.py`](AllFunction.py)文件中修改`self.temp_file_save_time`变量的值，也可以选择关闭自动删除功能

## 后续计划

- [x] 支持自动删除`temp`文件夹下的文件
- [x] 推理参数写入wav文件的元数据，支持读取
- [ ] 统一储存筛选出的音频文件
- [ ] 实现查看音频元数据的页面

……
