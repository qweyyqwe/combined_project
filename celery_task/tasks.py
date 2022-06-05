# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : tasks.py
# @Software: PyCharm


import time
import os

from celery_task import celery_app
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "property.settings")
django.setup()
# @app.task 指定将这个函数的执行交给celery异步执行


@celery_app.task
def test(mobile, code):
    print('1111')
    print(mobile,code)
    time.sleep(15)
    return mobile + code


@celery_app.task(name='send_email')
def send_email():
    print('发送运输邮件')


@celery_app.task(name='send_email2')
def send_email2():
    print('发送到站邮件')


