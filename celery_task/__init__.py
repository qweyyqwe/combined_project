# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : __init__.py.py
# @Software: PyCharm


from celery import Celery

celery_app = Celery('mycelery')
celery_app.config_from_object('celery_task.config')

