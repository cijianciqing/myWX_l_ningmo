# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         myFile
# Description:  
# Author:       Administrator
# Date:         2020-01-01
#-------------------------------------------------------------------------------
import uuid,time, random, string

from django.db import models


def image_upload_to(instance, filename):
    today = time.strftime("%F")
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    newKey = filename[-20:]
    filename01 = today + "---" + ran_str + "---" + newKey
    return 'weixinFiles/{filename}'.format(filename=filename01)





class WeiXinFile(models.Model):
    WeiXinFile_Types = (
        ('image', 'image'),
        ('video', 'video'),
        ('document', 'document'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=WeiXinFile_Types,default="image")
    file = models.FileField(upload_to=image_upload_to)
    # 图片得票数
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name