# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import Truck, Driver, MailRecord
from rest_framework import serializers


class TruckSer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = "__all__"


class DriverSer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class MailRecordSer(serializers.ModelSerializer):
    class Meta:
        model = MailRecord
        fields = "__all__"