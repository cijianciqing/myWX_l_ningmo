# -*- encoding=utf-8 -*-

import json
import requests
from utils import proxy
import myWX_l_ningmo.settings

import logging

logger = logging.getLogger('django')

def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, myWX_l_ningmo.settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())

    data = json.loads(response.text)
    logger.info('result from weixinServer : ',data)
    return data
