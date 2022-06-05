# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : pay_url.py
# @Software: PyCharm


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('create_order/', views.CreateOrder.as_view()),
    path('good/', views.Good.as_view()),
    path('callback/', views.Hui.as_view()),
]
