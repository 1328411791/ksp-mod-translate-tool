import string

from zhipuai import ZhipuAI
from tools.TranslationTools import TranslationTools


class ZhipuTool(TranslationTools):
    api_key = "ec27e0c61afe9bbd575a65eda2839311.QZU1TVaZbnDDLYSX"

    global client

    def __init__(self, token):
        self.client = ZhipuAI(api_key=token)
        self.name = "ZhipuTool"
        super().__init__()

    def create_request(self, word):
        print(f"ZhipuTool: {word}")
        try:
            response = self.client.chat.completions.create(
                model="glm-4",  # 填写需要调用的模型名称
                messages=[
                    {"role": "system", "content": "作为一名翻译人员，请给坎巴拉太空计划的模组翻译文本，请将这段话翻译为中文，不输出任何提示语言，不输出任何格式文本，只输出翻译文本。"
                                                  "如果无法直接翻译，则只输出对应的原文,同样不输出任何格式文本和提示语，只输出翻译文本。"},
                    {"role": "user", "content": word}
                ]
            )
        except Exception as e:
            print(f"ZhipuTool: {e}")
            return None
        return response.choices[0].message

    def translate_word(self, word):
        request = self.create_request(word)
        return request.content
