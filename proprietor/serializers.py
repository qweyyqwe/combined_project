# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : serializers.py
# @Software: PyCharm

from .models import RepairInto
from rest_framework import serializers


class RepairIntoSer(serializers.ModelSerializer):
    class Meta:
        model = RepairInto
        fields = "__all__"
