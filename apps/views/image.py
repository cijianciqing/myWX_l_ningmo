#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : imooc
# @Email          : imooc@foxmail.com
# @Created at     : 2018/11/30
# @Filename       : image.py
# @Desc           :


import os
import hashlib
from django.views import View
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from myWX_l_ningmo import settings
import utils
from utils.myResponse import ReturnCode, CommonResponseMixin
import logging

logger = logging.getLogger('django')




class ImageView(View, CommonResponseMixin):
    def get(self, request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')


        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)

    #上传文件
    def post(self, request):
        files = request.FILES
        response_data = []
        for key, uploaded_file in files.items():
            logger.info('image file from weixin, key is : ' + key)
            content = uploaded_file.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            logger.info('image file from weixin, md5 is : ' + md5)
            with open(path, 'wb+') as f:
                f.write(content)
            response_data.append({
                'name': key,
                'md5': md5
            })
        response = self.wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

    #删除文件
    def delete(self, request):
        md5 = request.GET.get('md5')
        img_name = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, img_name)
        if os.path.exists(path):
            os.remove(path)
            message = 'remove success.'
        else:
            message = 'file(%s) not found.' % img_name
        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response, safe=False)
