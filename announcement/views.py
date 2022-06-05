from django.shortcuts import render

# Create your views here.


import traceback

# 内置
import uuid
import re
import os
import redis

from django.shortcuts import redirect

from utils.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template import Context, loader
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from linecache import cache
from django.contrib.auth.hashers import make_password, check_password

# 本地导包
from utils.jwt import jwt_token
from account.models import Account, UserGroup
from utils.public import xtree
from utils.account_login import get_resource_list, menu_left_list
from utils.redis_cache import mredis
from .models import Announcement


# 用户发布公告
class AddAnnouncement(APIView):
    def post(self, request):
        data = request.data
        pass









