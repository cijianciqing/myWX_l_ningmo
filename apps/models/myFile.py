# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         myFile
# Description:  
# Author:       Administrator
# Date:         2020-01-01
#-------------------------------------------------------------------------------
from django.db import models


class WeiXinFile(models.Model):
    WeiXinFile_Types = (
        ('image', 'image'),
        ('video', 'video'),
        ('document', 'document'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=WeiXinFile_Types,default="image")
    file = models.FileField(upload_to="weixinFiles")

    def __str__(self):
        return self.name