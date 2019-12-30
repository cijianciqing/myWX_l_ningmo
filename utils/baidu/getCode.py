# -*- encoding=utf-8 -*-

import json
import requests
from utils import proxy
import myWX_l_ningmo.settings

import logging

logger = logging.getLogger('django')

def getCode(appid, code):
    logger.info('Baidu start get Code from BaiduGetCode ')
    API = 'http://openapi.baidu.com/oauth/2.0/authorize'
    params = 'response_type=code&client_id=%s&redirect_uri=%s&scope=email&display=popup' % \
             (myWX_l_ningmo.settings.Baidu_API_Key,myWX_l_ningmo.settings.Baidu_RedirectUri)
    url = API + '?' + params
    response = requests.get(url=url)

    data = json.loads(response.text)
    logger.info('Baidu result from BaiduGetCode : ',data)
    return data

