# -*- encoding=utf-8 -*-

import json
import requests
from utils import proxy
import myWX_l_ningmo.settings

import logging

logger = logging.getLogger('django')

def getToken(code):
    logger.info('Baidu getToken start')
    API = 'https://openapi.baidu.com/oauth/2.0/token'
    params = 'grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % \
             (code,myWX_l_ningmo.settings.Baidu_API_Key,myWX_l_ningmo.settings.Baidu_Secret_Key,myWX_l_ningmo.settings.Baidu_RedirectUri)
    url = API + '?' + params
    response = requests.get(url=url)

    data = json.loads(response.text)

    logger.info('Baidu result from BaiduGetToken : ', data)
    return data
