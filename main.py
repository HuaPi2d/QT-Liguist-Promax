from googletrans import Translator
from translate_api import translate_text
from file_ts import read_ts_file, get_target_language, get_unfinished_translation_units, get_translation_units, write_ts_file
import asyncio
import json
import tqdm
from concurrent.futures import ThreadPoolExecutor


def translate_worker(tu, target_language):
    '''
    翻译单个条目
    '''
    if tu["translation"] == None:
        try:
            tu["translation"] = asyncio.run(translate_text(tu["source"], target_language))
        except:
            pass
    return tu


def translate_ts_file(ts_file_path, json_file_path):
    # 读取翻译文件
    root = read_ts_file(ts_file_path)
    # 获取目标语言
    target_lang = get_target_language(root)
    # 获取翻译单元
    translation_units = get_translation_units(root)
    result_list = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        tasks = [executor.submit(translate_worker, tu, target_lang) for tu in translation_units]

        for task in tqdm.tqdm(tasks, desc='翻译中...'):
            result_list.append(task.result())
    # 写入 json 文件
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(result_list, json_file, ensure_ascii=False, indent=4)


def write_into_ts_file(ts_file_path, json_file_path, new_ts_file_path):
    # 读取 ts 文件
    root = read_ts_file(ts_file_path)
    # 读取 json 文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data_list = json.load(f)
    # 写入 ts 文件
    write_ts_file(new_ts_file_path, root, json_data_list)


# 启动异步事件循环
if __name__ == "__main__":
    ts_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh.ts'
    json_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh.json'
    new_ts_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh_new.ts'
    translate_ts_file(ts_file_path, json_file_path)
    write_into_ts_file(ts_file_path, json_file_path, new_ts_file_path)

