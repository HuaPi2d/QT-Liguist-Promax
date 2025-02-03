# `QT-Liguist-Promax`

---

[TOC]

---

## 一、使用须知

> 本项目使用了 `googletrans` 库，因此在使用时需要搭梯子

## 二、用户自定义参数（部分参数必须进行设置）

> 此项目中有一些参数可以根据用户具体需求进行调整

### 1. 文件路径（必须设置）

> 在 `main.py` 的入口函数中存在如下参数：
>
> ```python
> ts_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh.ts'
> json_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh.json'
> new_ts_file_path = 'D:\VS code\projects\HuaPi_so\language\Translation_zh_new.ts'
> ```
>
> - `ts_file_path` ：待处理的 `.ts` 文件路径
>
> - `json_file_path` ：中间翻译结果文件的存储路径
>
> 	```json
> 	[
> 	    {
> 	        "source": "颜色选择器",
> 	        "translation": "ColorPicker"
> 	    },
> 	    {
> 	        "source": "ColorPickerDialog",
> 	        "translation": "ColorPickerDialog"
> 	    },
> 	    {
> 	        "source": "警告",
> 	        "translation": "warn"
> 	    },
> 	    {
> 	        "source": "文件名不能为空！",
> 	        "translation": "The file name cannot be empty!"
> 	    },
> 	    {
> 	        "source": "文件已经存在！",
> 	        "translation": "The file already exists!"
> 	    }
> 	]
> 	```
>
> - `new_ts_file_path` ：翻译完成的 `.ts` 文件的路径（**不要与原文件路径相同，防止原文件损坏**）

### 2. 目标语言（推荐检查）

> 在 `.ts` 文件的开头有以下几个标签
>
> ```xml
> <?xml version="1.0" encoding="utf-8"?>
> <!DOCTYPE TS>
> <TS version="2.1" language="zh">
> ```
>
> 需要注意的是：`language` 属性，这里 `zh` 表示的是这是中文翻译文件，但 `google` 的翻译接口无法识别这一标识为中文。所以需要修改 `file_ts.py` 下的 `get_target_language` 函数
>
> ```python
> def get_target_language(root):
>     """
>     获取目标语言
>     """
>     if root.get("language") == "zh":
>         return "zh_CN"
>     return root.get("language")
> ```
>
> 这样就可以正常进行翻译。

### 3. 线程数

> 在 `main.py` 中的 `translate_ts_file` 函数下，存在语句：
>
> ```python
> with ThreadPoolExecutor(max_workers=50) as executor:
>     tasks = [executor.submit(translate_worker, tu, target_lang) for tu in translation_units]
> 
>     for task in tqdm.tqdm(tasks, desc='翻译中...'):
>         result_list.append(task.result())
> ```
>
> - `max_workers` ：默认同时执行线程数为 50（可以根据用户网络情况和电脑配置自行修改）