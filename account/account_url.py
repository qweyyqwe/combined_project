# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : account_url.py
# @Software: PyCharm


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),
    # 权限
    path('get_user_group/', views.GetUserRolesList.as_view()),

    # 增删改查    菜单
    path('get_menu/', views.GetMenuList.as_view()),
    path('add_menu/', views.AddMenu.as_view()),
    path('put_menu/', views.PutMenu.as_view()),
    path('del_menu/', views.DeleteMenu.as_view()),

    # 图片验证码
    path('image/', views.Image.as_view()),

    # path('email/', views.Email.as_view()),

    path('get_put_password/', views.GetPutPassword.as_view()),
    path('get_password', views.PutPassword.as_view()),
    path('put_pwd/', views.Validate.as_view()),

    # 异步邮箱



]
