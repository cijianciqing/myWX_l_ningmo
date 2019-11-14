from django.db import models

# Create your models here.
from apps.models import App


class User(models.Model):
    # open_id
    open_id = models.CharField(max_length=64, unique=True)
    # 昵称,db_index创建索引
    nickname = models.CharField(max_length=256, db_index=True)
    # 菜单app
    menu = models.ManyToManyField(App)
    '''
    # 关注的城市
    focus_cities = models.TextField(default='[]')
    # 关注的星座
    focus_constellations = models.TextField(default='[]')
    # 关注的股票
    focus_stocks = models.TextField(default='[]')

   

    class Meta:
        # 设置index
        indexes = [
            # models.Index(fields=['nickname'])
            models.Index(fields=['open_id', 'nickname'])
        ]
'''
    def __str__(self):
        return '%s' % (self.nickname)

    #用户默认拥有图片上传的应用
    # def myInit(self):
    #     initMenu = []
    #     imageApp = App.objects.get(appid='549eaaf72cb23716e2b1313acfaed23c')#图片上传
    #     print("this is myInit method in User: ",imageApp.to_dict())
    #     initMenu.append(imageApp.to_dict())
    #     self.menu.set(initMenu)

        # focus_menu = []
        # for item in post_menu:
        #     item = App.objects.get(appid=item.get('appid'))
        #     focus_menu.append(item)
        # user.menu.set(focus_menu)
        # user.save()


    # def __repr__(self):
    #     #     return self.nickname

