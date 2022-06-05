# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import User, Record
from rest_framework import serializers


class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RecordSer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"
