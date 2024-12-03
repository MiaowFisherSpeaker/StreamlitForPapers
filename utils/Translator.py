# -*- coding: utf-8 -*-
import json
import sys
import uuid
import requests
import hashlib
from importlib import reload

import time
from config import CONFIG

reload(sys)
'''
API文档
https://ai.youdao.com/DOCSIRMA/html/自然语言翻译/API文档/文本翻译服务/文本翻译服务-API文档.html'''

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]



class YouDaoFanYi:
    def __init__(self, YOUDAO_URL='https://openapi.youdao.com/api', APP_KEY=CONFIG.APP_KEY,
                 APP_SECRET=CONFIG.APP_SECRET):
        self.YOUDAO_URL = YOUDAO_URL
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def connect_trans(self, q1):
        q = q1
        data = {}
        data['from'] = 'en'
        data['to'] = 'zh_CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + truncate(q) + salt + curtime + self.APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = "您的用户词表ID"

        response = self.do_request(data)
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            millis = int(round(time.time() * 1000))
            filePath = "./miaow" + str(millis) + ".mp3"
            fo = open(filePath, 'wb')
            fo.write(response.content)
            fo.close()
        else:
            content = json.loads(response.content)
            # print(content['web'])
            # print(content['dict']['url'])
            # print(content['dict']['url'])
            # print(content['translation'][0])
            return content['translation'][0]


if __name__ == '__main__':
    Trans = YouDaoFanYi()
    print(Trans.connect_trans("hello world"))