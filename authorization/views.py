# -*- encoding=utf-8 -*-


import json

from django.http import JsonResponse
from django.views import View

from apps.models import App
from utils.myResponse import wrap_json_response, ReturnCode, CommonResponseMixin
from utils.auth import  c2s,already_authorized

from .models import User
import logging

logger = logging.getLogger('django')

def authorize(request):
    return __authorize_by_code(request)

def __authorize_by_code(request):
    if(request.session.session_key is not None):
        logger.info('session content in auth/authorize01: '+ request.session.session_key)
    # , " : " + request.session.items()
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    code = post_data.get('code').strip()
    if not (app_id and code):
        response['result_code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        # 标准微信访问
        data = c2s(app_id, code)
    except Exception as e:
        print("exception occured: ",e)
        response['result_code'] = ReturnCode.FAILED
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    open_id = data.get('openid')
    if not open_id:
        response['result_code'] = ReturnCode.FAILED
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['open_id'] = open_id
    request.session['is_authorized'] = True
    if (request.session.session_key is not None):
        logger.info('session content in auth/authorize01: ' + request.session.session_key)

    # User.objects.get(open_id=open_id) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not User.objects.filter(open_id=open_id):
        if nickname != "宁默":
            response['result_code'] = ReturnCode.FAILED
            response['message'] = 'You are not my kids.'
            return JsonResponse(response, safe=False)
        else:
            new_user = User(open_id=open_id, nickname=nickname)
            # 初始化新用户
            new_user.save()
            # 默认情况下为用户添加“图片上传功能”
            initMenu = []
            imageApp = App.objects.get(appid='549eaaf72cb23716e2b1313acfaed23c')  # 图片上传
            # print("this is myInit method in User: ", imageApp.to_dict())
            initMenu.append(imageApp)
            new_user.menu.set(initMenu)
            # print("add new user : ",new_user.nickname)
            logger.info("add a new user : " + new_user.nickname)


    message = 'user authorize successfully.'
    response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)

def logout(request):
    '''
    注销，小程序删除存储的Cookies
    '''
    for key, value in request.session.items():
        logger.info('session content in auth/logout: %s : %s' % (key, value))
    request.session.clear()
    if(request.session.items() is not None):
        for key, value in request.session.items():
            logger.info('session content2 in auth/logout: %s : %s' % (key, value))
    response = {}
    response['result_code'] = 0
    response['message'] = 'logout success.'
    return JsonResponse(response, safe=False)

# 判断是否已经登陆
def get_status(request):
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)