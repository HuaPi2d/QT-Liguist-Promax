import os
import sys
import xml.etree.ElementTree as ET


def read_ts_file(file_path):
    """
    读取ts文件，返回文件内容
    """
    with open(file_path, 'r',  encoding='utf-8') as f:
        content = f.read()

    root = ET.fromstring(content)
    return root

def write_ts_file(save_path, root, translation_units):
    """
    写入ts文件
    file_path: 文件路径
    root: xml根节点
    translation_units: 翻译单元列表
    """
    # 获取 message 节点列表
    message_list = root.findall('context/message')
    # 遍历翻译单元列表，更新 message 节点
    for translation_unit in translation_units:
        for message in message_list:
            if message.find("source").text == translation_unit["source"]:
                translation_node = message.find("translation")
                translation_node.text = translation_unit["translation"]
                if "type" in translation_node.attrib:
                    del message.find("translation").attrib['type']
    # 保存文件
    tree = ET.ElementTree(root)
    tree.write(save_path, encoding='utf-8', xml_declaration=True)


# <?xml version="1.0" encoding="utf-8"?>
# <!DOCTYPE TS>
# <TS version="2.1" language="en_US">

def get_target_language(root):
    """
    获取目标语言
    """
    if root.get("language") == "zh":
        return "zh_CN"
    return root.get("language")


# <context>
#     <name>ColorPickerDialog</name>
#     <message>
#         <location filename="../subwidgets/Dialog/color/colorpickerdialog.cpp" line="9"/>
#         <source>颜色选择器</source>
#         <translation>ColorPicker</translation>
#     </message>
# </context>


def get_translation_units(root):
    """
    获取翻译单元列表
    """
    message_list = root.findall('context/message')
    translation_units = [{"source": message.find("source").text, "translation": message.find("translation").text} for message in message_list]
    return translation_units


def get_unfinished_translation_units(root):
    """
    获取未翻译的翻译单元
    """
    message_list = root.findall('context/message/translation[@type="unfinished"]/..')
    translation_units = [{"source": message.find("source").text, "translation": message.find("translation").text} for message in message_list]
    return translation_units

