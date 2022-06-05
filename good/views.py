from django.shortcuts import render
# Create your views here.


import datetime
import math
import time
import random
import traceback

from django.http import HttpResponse
from .models import User, Record, TypeMoney
from .serializers import UserSer, RecordSer
from pay.models import Order
from pay.serializers import OrderSer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView


# 展示业主
# class Lei(ListAPIView):
#     serializer_class = RecordSer
#     queryset = Record.objects.all()


class Lei(APIView):
    def get(self, request):
        # car = Record.objects.filter(out_time=None)
        car = Record.objects.all().order_by('-pk')
        ser = RecordSer(car, many=True)
        return Response({"car_list": ser.data})


class AddUser(APIView):
    """
    添加业主
    获取前端数据

    """

    def post(self, request):
        name = request.data.get('name')
        car_number = request.data.get('car_number')
        type = request.data.get('type')
        if not all([name, car_number, type]):
            return Response({'msg': '车辆表的信息不全，请补全', "code": 400})
        if len(name) > 30:
            return Response({'msg': '业主名过长,请重新输入', "code": 400})
        if len(car_number) > 30:
            return Response({'msg': '车牌号过长,请重新输入', "code": 400})
        car_num = User.objects.filter(car_number=car_number).count()
        if car_num > 0:
            return Response({'msg': '该车辆已被注册，请重新确认', "code": 400})
        if type not in [1, 2]:
            return Response({'msg': '该类型不正确', "code": 400})
        User.objects.create(name=name, car_number=car_number, type=type)
        return Response({'msg': '业主信息录入成功', "code": 200})


# 进入
class CarGo(APIView):
    def post(self, request):
        car = request.data.get("car")
        print(car, "12321312")
        if not all([car]):
            return Response({'msg': '车辆表的信息不全，请补全', "code": 400})
        if len(car) > 30:
            return Response({'msg': '车牌号过长,请重新输入', "code": 400})
        record_num = Record.objects.filter(car=car, out_time=None).count()
        if record_num > 0:
            return Response({'msg': '该车辆已进入', "code": 400})
        time = datetime.datetime.now()
        Record.objects.create(car=car, in_time=time)
        return Response({'msg': '车辆信息录入成功', "code": 200})


# 离开
class Logout(APIView):
    def post(self, request):
        # 接收参数，并校验
        record_id = request.data.get("order_id")
        print(record_id)
        if not all([record_id]):
            return Response({'msg': '车辆表的信息不全，请补全', "code": 400})
        # 查询是否进入
        record_num = Record.objects.filter(id=record_id, out_time=None).count()
        if record_num == 0:
            return Response({'msg': '该车辆进入未登记', "code": 400})

        record = Record.objects.get(id=record_id, out_time=None)
        out_time = record.out_time
        if out_time:
            record_outtime = Record.objects.filter(Q(out_time != ''))
            return Response({'code': 400, 'msg': '该车已离开'})
        # 获取时间，计算停留时间
        out_time = datetime.datetime.now()  # 2022-05-20 10:14:57.614513
        in_time = record.in_time    # 2022-05-20 09:59:17.899571+00:00
        now3 = in_time.replace(tzinfo=None)     # 2022-05-20 09:59:17.899571
        time = (out_time - now3).seconds / 3600     # 0.2608333333333333
        time = math.ceil(time)
        # print("程序运行时间：" + str((out_time - in_time).seconds) + "秒")
        # 判断支付类型
        try:
            type1 = ""
            car_num = User.objects.filter(car_number=record_id).count()
            if car_num == 0:
                type1 = 3
            else:
                user = User.objects.get(car_number=record_id)
                if user.type == 1:
                    type1 = 1
                elif user.type == 2:
                    type1 = 2
            # 计算费用
            type = TypeMoney.objects.get(type=type1)
            price = type.money
            money = time * price
            print("类型", type1, "单价", price, "费用", money)
            # 写入数据库
            record.money = money
            record.out_time = out_time
            record.save()
            # # 生成订单
            # # 订单的唯一标识
            # # 随机数     时间戳
            # code = car + str(random.randint(10000, 99999))
            # print(code)
            # # 生成订单
            # order = Order.objects.create(order_code=code, car_count=car, total_pay=money)
            # order.save()
            return Response({'msg': '车辆信息录入成功', "code": 200})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({"code": 406})


class ShowCarRecord(APIView):
    def get(self, request):
        record_car = Record.objects.all()
        record_car_list = RecordSer(record_car, many=True)
        return Response({'code': 200, "record": record_car_list})


class ShowCarOrder(APIView):
    def get(self, request):
        order_car = Order.objects.all()
        order_list = OrderSer(order_car, many=True)
        return Response({"order": order_list})

