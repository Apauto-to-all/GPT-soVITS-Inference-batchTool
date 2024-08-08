# 处理元数据
import json
import requests

# 用于写入读取元数据
from mutagen.wave import WAVE
from mutagen.id3 import TXXX

# 继承所有设置用的数据
from link_utils import LinkUtils


class MetadataWav(LinkUtils):
    def __init__(self):
        super().__init__()
        self.main_setting

    # 写入元数据，wav文件，写入元数据
    def add_metadata_to_wav(self, wav_path, metadata_dict):
        # 读取wav文件
        audio = WAVE(wav_path)
        # 初始化标签，如果没有标签
        if audio.tags is None:
            audio.add_tags()
        # 将url编码的文本解码
        metadata_dict["text"] = requests.utils.unquote(metadata_dict["text"])
        # 将字典转换为JSON字符串
        metadata_json = json.dumps(metadata_dict, ensure_ascii=False)
        # 使用 TXXX 帧来存储自定义元数据
        audio.tags.add(TXXX(encoding=3, desc="tts_parameters", text=metadata_json))
        audio.save()  # 保存元数据

    # 从wav文件中读取元数据
    def read_metadata_from_wav(self, wav_path):
        # 读取元数据
        audio = WAVE(wav_path)
        # 如果没有标签，返回空字典
        tts_parameters = next(
            (
                tag.text[0]  # 返回TXXX标
                for tag in audio.tags.values()  # 遍历所有标签
                if isinstance(tag, TXXX)
                and tag.desc
                == "tts_parameters"  # 如果是TXXX标签，并且描述为tts_parameters
            ),
            None,  # 如果没有找到，返回None
        )
        return json.loads(tts_parameters) if tts_parameters else {}  # 返回元数据
