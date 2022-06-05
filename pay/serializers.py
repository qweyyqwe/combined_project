# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import Order
from rest_framework import serializers


class OrderSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
