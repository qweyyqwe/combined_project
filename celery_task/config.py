# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : config.py
# @Software: PyCharm


BROKER_URL = 'redis://127.0.0.1:6379/11'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/12'
# 时区
timenzone = 'Asia/Shanghai'

# 导入指定的任务模块
CELERY_IMPORTS = (
    'celery_task.tasks',
)
