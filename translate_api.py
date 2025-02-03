from googletrans import Translator


async def translate_text(text, target_language):
    # 创建Translator对象
    translator = Translator()
    # 使用translate方法进行翻译，必须使用await来等待
    translation = await translator.translate(text, dest=target_language)
    return translation.text