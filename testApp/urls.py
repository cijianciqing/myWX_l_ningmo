"""myWX_l_ningmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from testApp import views

urlpatterns = [
    path('test01',views.basicTest),
    path('test02',views.basicTest02),
    path('test03',views.basicTest03),
    path('test04',views.ResponseTest01.as_view()),
    path('testSession01', views.test_session),
    path('testSession02', views.test_session2),
    re_path('^$',views.index)
]
