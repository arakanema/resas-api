# coding: utf-8

import json
import requests
import numpy as np
import pandas as pd
from matplotlib import pyplot

EP = 'https://opendata.resas-portal.go.jp'
APIKEY = open('./api-key.txt').read()

url = '/'.join([EP, 'api/v1/employEducation/localjobAcademic/toTransition'])
headers = {'X-API-KEY': APIKEY}
payload = {
    'prefecture_cd': '44',
    'displayMethod': '0', # 0:実数 / 1:就職率・進学率
    'matter': '3', # 0:地元就職 / 1:流出 / 2:流入 / 3:純流入
    'classification': '0', # 0:就職・進学の合計 / 1:進学 / 2:就職
    'displayType': '00', # 00:すべての就職・進学 / 10:すべての進学 / 11:大学進学 / 12:短期大学進学 / 20:就職
    'gender': '2' # 0:総数 / 1:男性 / 2:女性
}
rs = requests.get(url, params=payload, headers=headers)
result = json.loads(rs.text)
if result['message']:
    print(result['message'])
else:
    df = pd.DataFrame(result['result']['changes'][0]['data'])
    print(df)
    # df2 = pd.DataFrame(result['result']['changes'][1]['data'])
    # print(df2)



