# coding: utf-8

"""
RESAS API 利用に必要な都道府県コード・市区町村コードの取得
"""

import requests
import json
import time
import numpy as np
import pandas as pd

EP = 'https://opendata.resas-portal.go.jp'
APIKEY = open('./api-key.txt').read()

def get_pref_code(ep, api_key):
    url = '/'.join([ep, 'api/v1/prefectures'])
    headers = {'X-API-KEY': api_key}
    rs = requests.get(url, headers=headers)
    result = json.loads(rs.text)
    if result['message']:
        print(result['message'])
    else:
        df = pd.DataFrame(result['result'])
        df.set_index('prefCode', inplace=True)
        return df


def get_city_code(ep, api_key, pref_code):
    url = '/'.join([ep, 'api/v1/cities'])
    headers = {'X-API-KEY': api_key}
    payload = {'prefCode': pref_code}
    rs = requests.get(url, headers=headers, params=payload)
    result = json.loads(rs.text)
    if result['message']:
        print(result['message'])
    else:
        df = pd.DataFrame(result['result'])
        return df


def init():
    pref = get_pref_code(EP, APIKEY)
    pref.to_csv('./codes/prefCode.csv', index=False, encoding='utf-8')
    all_cities = pd.DataFrame()
    for pref_code in pref.index:
        city = get_city_code(EP, APIKEY, pref_code)
        if all_cities.empty:
            all_cities = city
        else:
            all_cities = pd.concat([all_cities, city])
    all_cities.set_index(['prefCode', 'cityCode'])
    all_cities.to_csv('./codes/cityCode.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    init()