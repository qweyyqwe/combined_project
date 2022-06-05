# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : celery.py
# @Software: PyCharm


# import os
# from celery import Celery
# from django.conf import settings
#
# # 设置celery的环境变量和django-celery的工作目录
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "property.settings")
# # 实例化celery应用，传入服务器名称
# app = Celery("property")
# # 加载celery配置
# app.config_from_object("django.conf:settings")
#
# # 如果在项目中，创建了task.py,那么celery就会沿着app去查找task.py来生成任务
# # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# # 加载任务
# # 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# # app.autodiscover_tasks(["任务1","任务2"])
# app.autodiscover_tasks(["app_task", ])
#
# # CELERYD_CONCURRENCY = 1  # 并发worker数
# CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
# CELERY_ENABLE_UTC = False  # 禁止使用时间
