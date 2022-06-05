# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import Resource, UserGroup, Menu, Account
from rest_framework import serializers


class ResourceSer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class UserGroupSer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = "__all__"


class MenuSer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class AccountSer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
