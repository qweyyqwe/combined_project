# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : proprietor_url.py
# @Software: PyCharm


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    # 添加区域
    path('add_area/', views.AddArea.as_view()),
    path('put_area/', views.PutArea.as_view()),
    # 完善房屋信息
    path('add_house/', views.AddHouse.as_view()),
    path('add_repair/', views.AddRepairInto.as_view()),
    # 分配维修
    path('allot_repair/', views.AllotRepair.as_view()),
    path('get/', views.Get.as_view()),
    # 对应维修员的工作
    path('maintainer_list/', views.MaintainerList.as_view()),
    path('maintainer_work/', views.MaintainerWork.as_view()),
    path('maintainer_out_work/', views.MaintainerOutWork.as_view()),

]
