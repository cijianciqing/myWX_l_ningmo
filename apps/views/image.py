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

#无用方法，已通过class ImageView（）进行优化
# def image(request):
#     if request.method == 'GET':
#         md5 = request.GET.get('md5')
#         imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
#         print(imgfile)
#         if os.path.exists(imgfile):
#             data = open(imgfile, 'rb').read()
#             # return HttpResponse(data, content_type='image/jpg')
#             return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
#         else:
#             return Http404()
#     elif request.method == 'POST':
#         pass
#
#
# def image_text(request):
#     if request.method == 'GET':
#         md5 = request.GET.get('md5')
#         imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
#         if not os.path.exists(imgfile):
#             return utils.response.wrap_json_response(
#                 code=utils.response.ReturnCOde.RESOURCES_NOT_EXISTS)
#         else:
#             response_data = {}
#             response_data['name'] = md5 + '.jpg'
#             response_data['url'] = '/service/image?md5=%s' % (md5)
#             response = utils.response.wrap_json_response(data=response_data)
#             return JsonResponse(data=response, safe=False)


class ImageView(View, CommonResponseMixin):
    def get(self, request):
        # 判断是否处于认证状态
        # if not utils.auth.already_authorized(request):
        #     response = self.wrap_json_response({}, code=ReturnCode.UNAUTHORIZED)
        #     return JsonResponse(data=response, safe=False)
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')

        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            # return HttpResponse(data, content_type='image/jpg')
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)

    #上传文件
    def post(self, request):
        files = request.FILES
        response_data = []
        # print(files['test'])
        for key, uploaded_file in files.items():
            logger.info('image file from weixin, key is : ',key)
            logger.info('image file from weixin, uploaded_file is : ',uploaded_file)
            content = uploaded_file.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            print('image file from weixin, md5 is : ',md5)
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
