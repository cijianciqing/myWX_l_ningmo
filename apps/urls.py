

from django.urls import path,include
from .views import menu,image

urlpatterns = [
    path('menu/list', menu.get_menu),
    path('menu/user', menu.UserMenu.as_view()),
    path('image', image.ImageView.as_view()),
]