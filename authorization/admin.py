from django.contrib import admin

# Register your models here.
from authorization.models import User


@admin.register(User)
class AuthorizationUserAdmin(admin.ModelAdmin):
    pass
    # exclude之后，admin后台就不显示此属性了
    # exclude = ['open_id']
