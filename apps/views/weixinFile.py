# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         weixinFile
# Description:  
# Author:       Administrator
# Date:         2020-01-01
#-------------------------------------------------------------------------------


from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from myWX_l_ningmo import settings
import time
import logging
import os
from utils.myResponse import wrap_json_response, ReturnCode
#生成随机数
import random, string
from ..models.myFile import WeiXinFile

logger = logging.getLogger('django')

imageType = ['jpg', 'png', 'gif']
videoType = ['mp4', 'avi', 'mpg']
documentType = ['docx', 'xdml','pdf']


#保存微信文档
#最新版
def saveWX(request):
    today = time.strftime("%F")
    files = request.FILES
    response_data = []
    for key, uploaded_file in files.items():

        newKey = key[-20:]
        fileType = os.path.splitext(newKey)[-1][1:]
        if(fileType in videoType):
            fileType='video'
        elif(fileType in documentType):
            fileType = 'video'
        else:
            fileType = 'image'
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        filename = today + "---" + ran_str + "---" + newKey

        weixinFile = WeiXinFile()
        weixinFile.name = filename
        weixinFile.file = uploaded_file
        weixinFile.type = fileType
        weixinFile.save()
        response_data.append({
            'name': key,
            'md5': filename
        })
    response = wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

#老版
# def saveWX(request):
#     # %F 年-月-日
#     #'2019-12-31'
#     today = time.strftime("%F")
#     files = request.FILES
#     response_data = []
#     for key, uploaded_file in files.items():
#         logger.info('image file from weixin, key is : ' + key)
#         newKey = key[-20:]
#         ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#
#         path = os.path.join(settings.IMAGES_DIR, today + "---" + ran_str + "---" +  newKey)
#         logger.info('image file from weixin, md5 is : ' + path)
#         with open(path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
#         response_data.append({
#             'name': key,
#             'md5': path
#         })
#     response = wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
#     return JsonResponse(data=response, safe=False)

#获取最近上传的10个文件

def getRecentWX(request):
    # 暂且设置，只获取图片
    recentFiles = WeiXinFile.objects.filter(type='image').order_by('votes')[:10]
    imageList = []
    videoList = []
    response_data = []
    for file01 in recentFiles:
        json_dict = {}
        json_dict["name"] = file01.name
        json_dict["url"] = settings.MyServerPrefix + file01.file.url
        logger.info(file01.file.url)
        if(file01.type=='image'):
            imageList.append(json_dict)
        else:
            videoList.append(json_dict)
    logger.info('2222')
    response_data.append({
        'imageList': imageList,
        'videoList': videoList
    })
    logger.info('1111')
    response = wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)