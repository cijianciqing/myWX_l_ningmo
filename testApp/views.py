import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse,JsonResponse, FileResponse
from django.views import View
from utils.baidu.getToken import getToken
from utils.baidu.getCode import getCode

import logging

logger = logging.getLogger('django')

def index(request):
    return render_to_response('testApp/myIndex.html', locals())

from utils.myResponse import wrap_json_response,CommonResponseMixin,ReturnCode
# Create your views here.
def basicTest(request):
    myresponse_content = 'this is just a test'
    return HttpResponse(myresponse_content)

def basicTest02(request):
    myresponse_content = {'data11': "aaa"}
    return JsonResponse(data=myresponse_content)

def basicTest03(request):
    myresponse_content = {'data22': "bbb"}
    myResponse_data = wrap_json_response(data=myresponse_content,code=ReturnCode.SUCCESS)
    return JsonResponse(data=myResponse_data,safe=False)

def testBaidu01(request):
    myCode = request.GET.get("code")
    logger.info("Baidu Return Code : ",myCode)
    getToken(myCode)


def testBaidu02(request):
    myCode = getCode()
    myresponse_content = {'data22': "aaaaaaaaa"}
    myResponse_data = wrap_json_response(data=myresponse_content, code=ReturnCode.SUCCESS)
    return JsonResponse(data=myResponse_data, safe=False)

class ResponseTest01(View, CommonResponseMixin):
    def get(self, request):
        myresponse_content = {'data33': "cccc"}
        myResponse_data = wrap_json_response(data=myresponse_content, code=ReturnCode.SUCCESS)
        return JsonResponse(data=myResponse_data, safe=False)

# 测试session
# 测试微信-django的 cookie--sesison
def test_session(request):
    request.session['message'] = 'Test Django Session OK!'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

# 测试微信-django的 cookie--sesison
def test_session2(request):
    print('session content: ', request.session.items())
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
