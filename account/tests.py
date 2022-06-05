from __future__ import absolute_import, unicode_literals
from django.test import TestCase

# Create your tests here.

# 绝对引用，使我们的celery模块不会与原始的celery冲突

# 导入原始的celery模块中shared_task    from xx import xx
from celery import shared_task
# 使用django内置函数发送邮件
from django.core.mail import send_mail
# 导入django的settings
from django.conf import settings


@shared_task
def send_mail_task(usernaem, email, token):
    """
    使用django内置函数发送邮件
    """
    subject = "海上明月"
    message = ""
    sender = settings.EMAIL_FROM
    recipient = [email]
    html_message = "<h1>{},欢迎您注册，请点击以下链接进行激活邮箱：<a href='http://127.0.0.1:8000/api/v1/active/{}'>点击这里进行激活</a></h1>".format(username, token)
    send_mail(subject, message, sender, recipient, html_message=html_message)
