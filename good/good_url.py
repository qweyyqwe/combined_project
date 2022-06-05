# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : good_url.py
# @Software: PyCharm


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('add_user/', views.AddUser.as_view()),
    path('add_car/', views.CarGo.as_view()),
    path('show_car/', views.Lei.as_view()),
    path('logout/', views.Logout.as_view()),
    path('show_car_record/', views.ShowCarRecord.as_view()),
    path('show_car_order/<str:s>/', views.ShowCarOrder.as_view()),
]
# router = DefaultRouter()
# router.register('user',views.UserViewSets)
# router.register('record',views.RecordViewSets)
# urlpatterns += router.urls

