# 有道翻译api
import json
import sys
import uuid
import requests
import hashlib
import time
from tools.TranslationTools import TranslationTools


class Youdao(TranslationTools):

    YOUDAO_URL = 'https://openapi.youdao.com/api'
    APP_KEY = ""
    APP_SECRET = ""

    def __init__(self, app_key, app_secret):
        self.APP_KEY = app_key
        self.APP_SECRET = app_secret
        super().__init__()

    def encrypt(self,signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def connect(self,text):

        data = {}
        data['from'] = 'en'
        data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(text) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = text
        data['salt'] = salt
        data['sign'] = sign

        response = self.do_request(data)

        # print(response.content ,"\n")
        # 解析返回结果
        rep = response.content.decode('utf-8')

        return rep

    def translate_word(self, text):
        # 解析json返回结果
        rep = self.connect(text)

        data = json.loads(rep)
        translation_result = data["translation"][0]
        # print(translation_result)
        # 休息0.5s
        time.sleep(0.5)

        return translation_result
