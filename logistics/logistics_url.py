# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : logistics_url.py
# @Software: PyCharm


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    # 添加车辆
    path('add_car/', views.AddCar.as_view()),
    # 添加司机
    path('add_truck/', views.AddDriver.as_view()),

    path('add_record/', views.AddMailRecord.as_view()),
    # 发快递
    path('show_into/', views.ShowCarDriver.as_view()),
    # 展示快递
    path('show_express/', views.ShowExpress.as_view()),
    # 发货
    path('deliver/', views.AdministratorAllExpress.as_view()),
    # 到达
    path('arrival/', views.ArrivalExpress.as_view()),
    # 收货
    path('sign/', views.Sign.as_view()),
    # 支付
    path('freight/', views.ExpressFreight.as_view()),
    # 快递到达 发送邮件通知
    # path('/', views.ArrivalEmail.as_view()),
    # 管理员
    path('show_all_express/', views.ShowAllExpress.as_view()),
    # 到达发送邮箱提醒 货到了
    path('finish_email/<int:id>', views.FinishEmail.as_view()),
    # path('finish_email/', views.FinishEmail.as_view()),




]
