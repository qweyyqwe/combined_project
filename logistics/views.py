from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.


import datetime
import math
import time
import random
import traceback

from django.http import HttpResponse
from pay.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView

from .models import Truck, Driver, MailRecord, Site
from .serializers import TruckSer, DriverSer, MailRecordSer
from utils.public import create_order
from celery_task.tasks import send_email, send_email2


class AddCar(APIView):
    """
    添加车辆
    """
    def post(self, request):
        data = request.data
        print(data)
        plate_number = data.plate_number
        status = data.status
        if not all([plate_number]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        plate_count = Truck.objects.get(plate_number=plate_number).count()
        if plate_count > 0:
            return Response({'msg': '该车辆已被注册，请补全', "code": 400})
        try:
            truck = Truck.objects.create(plate_number=plate_number, status=status)
            truck.save()
            return Response({'msg': '注册成功', "code": 200})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'msg': '注册异常', "code": 400})


class AddDriver(APIView):
    """
    添加司机
    """
    def post(self, request):
        data = request.data
        print(data)
        name = data.name
        phone = data.phone
        status = data.status
        if not all([name, phone]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        driver_count = Driver.objects.get(Q(name=name) | Q(phone=phone)).count()
        if driver_count > 0:
            return Response({'msg': '该名字或手机号已被注册', "code": 400})
        try:
            driver = Driver.objects.create(name=name, phone=phone, status=status)
            driver.save()
            return Response({'msg': '注册成功', "code": 200})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'msg': '注册异常', "code": 400})


class ShowCarDriver(APIView):
    """
    展示空闲的车和司机
    """
    def get(self, request):
        car = Truck.objects.filter(status=0)
        driver = Driver.objects.filter(status=0)
        car_ser = TruckSer(car, many=True)
        driver_ser = DriverSer(driver, many=True)
        return Response({"car_list": car_ser.data, "driver_list": driver_ser.data})


class AddMailRecord(APIView):
    """
    发快递
    """
    def post(self, request):
        data = request.data
        print(data)
        order_code = str(random.randint(1000, 9999)) + str(int(time.time()))
        print(order_code)
        name = request.data.get('name')
        sender = request.data.get('sender')
        receiver = request.data.get('receiver')
        truck = request.data.get('truck')
        driver = request.data.get('driver')
        to_place = request.data.get('to_place')
        from_place = request.data.get('from_place')
        if to_place == from_place:
            return Response({'code': 500, 'msg': '地址有误'})
        print(name, sender, receiver, truck, driver)
        if not all([order_code, name, sender, receiver, truck, driver]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        site = Site.objects.filter(go_site=to_place, from_site=from_place).first()
        # print('site>>>>>>', site.money)
        money = site.money
        # print(name, sender, receiver)
        # if not all([order_code, name, sender, receiver]):
        #     return Response({'msg': '信息不全，请补全', "code": 400})
        # 下拉
        # to_place = request.data.get('to_place')
        # from_place = request.data.get('from_place')
        try:
            MailRecord.objects.create(order_code=order_code, name=name, sender=sender, receiver=receiver,
                                      to_place=to_place, from_place=from_place, money=money, truck_id_id=truck, driver_id_id=driver)
            return Response({'code': 200, 'msg': '完成，快递等待揽收'})
        except:
            error = traceback.format_exc()
            print(error)
            return Response(error)


# TODO 展示自己快递
class ShowExpress(APIView):
    def get(self, request):
        express = MailRecord.objects.all()
        # express = MailRecord.objects.filter(Q(status=0) | Q(status=1))
        express_ser = MailRecordSer(express, many=True)
        # print(express_ser)

        # print(express_ser.status)
        return Response({"express_list": express_ser.data})


class Sign(APIView):
    """
    收货
    """
    def post(self, request):
        express = request.data.get('id')
        print(express)
        express_status = MailRecord.objects.get(id=express)
        express_status_now = express_status.status
        if express_status_now == 0:
            return Response({'code': 400, 'msg': '快递还为未发货'})
        elif express_status_now == 1:
            return Response({'code': 400, 'msg': '快递还在运输中'})
        elif express_status_now == 3:
            return Response({'code': 400, 'msg': '该快递已签收'})
        express_status.status = 2
        express_status.save()
        return Response({'code': 200, 'msg': '签收'})


# 获取到地址  取对应价格   支付价格
import random
from utils.keys.alipay import get_ali_object
class ExpressFreight(APIView):
    def post(self, request):
        print('支付》》》》》》》')
        order_id = request.data.get('id')
        print(order_id)
        order = MailRecord.objects.filter(id=order_id).first()
        if not order:
            return Response({'msg': '订单不存在', 'code': 500})
        order = MailRecord.objects.get(id=order_id)
        order_code = order.order_code
        # 从记录表获取价格
        record = MailRecord.objects.filter(id=order_id).first()
        money = record.money
        # TODO 调用get_ali_object()方法
        alipay = get_ali_object()
        # 生成支付的url
        try:
            query_params = alipay.direct_pay(
                subject="运费支付",  # 商品简单描述
                out_trade_no=order_code,  # 用户购买的商品订单号（每次不一样） 20180301073422891
                total_amount=int(money),  # 交易金额(单位: 元 保留俩位小数)
            )
            # print(query_params)
            pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
            order = MailRecord.objects.get(id=order_id)
            order.status = 2
            order.save()
            return Response({'pay_url': pay_url, 'code': 200})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'error': error})


# TODO  登录管理员可发货
class AdministratorAllExpress(APIView):
    def post(self, request):
        # 获取该用户是什么角色   2为管理员可发货
        """
             roles = 1
        if roles == 2:
            express_status = MailRecord.objects.get(status=0)
            if express_status.status == 1:
                return Response({'code': 400, 'msg': '该快递已在路上'})
            express_status.status = 1
            express_status.save()
            return Response({'code': 200, 'msg': '正在派送'})
`
        """
        express = request.data.get('id')
        express_status = MailRecord.objects.get(id=express)
        express_status.status = 1
        express_status.save()
        return Response({'code': 200, 'msg': '正在派送'})


# 到达  用户可领取
class ArrivalExpress(APIView):
    def post(self, request):
        express = request.data.get('id')
        express_status = MailRecord.objects.get(id=express)
        express_status.status = 2
        express_status.save()
        return Response({'code': 200, 'msg': '快递到达目的地'})


# TODO 管理员可查看所有  未发货的快递
class ShowAllExpress(APIView):
    def get(self, request):

        # 获取当前登录用户的用户名
        express = MailRecord.objects.filter(Q(status=0) | Q(status=1))
        # express = MailRecord.objects.filter(Q(status=0) | Q(status=1) | Q(username=name))
        express_ser = MailRecordSer(express, many=True)
        return Response({"express_list_all": express_ser.data})


from django.core import mail


# 开始时发送邮件
class ReceiverSendMail(APIView):
    def post(self, request, id):
        # 获取到这条数据

        mail_record_id = MailRecord .objects.filter(id=id)
        print('mail_record_id>>', mail_record_id)
        # 获取到收货人邮件
        receiver_mail = MailRecord.objects.get(id=id).receiver_email
        print('receiver_mail>>', receiver_mail)
        # send_email.delay()
        subject = '测试邮件主题'
        message = '快递已发货'
        from_email = 'yang_123456202204@163.com'
        to_email = receiver_mail    # 3413299451@qq.com
        result = send_mail(subject, message, from_email, [to_email])
        print('result>>>', result)
        return Response({'code': 200, 'data': result})


from django.template.loader import render_to_string
# 结束时发送邮件
class FinishEmail(APIView):
    def post(self, request):
        id = request.query_params.get('id')
        print(id)
        mail_record_id = MailRecord.objects.filter(id=id)
        print('mail_record_id>>', mail_record_id)
        # receiver_mail = MailRecord.objects.get(id=id).receiver_email
        # print('receiver_mail>>', receiver_mail)
        try:
            receiver_mail = '3413299451@qq.com'
            send_email2.delay()
            subject = '测试邮件主题'
            message = render_to_string('arrival.html'), {'name': mail_record_id.name, 'ordercode':
                mail_record_id.order_code, 'phone': mail_record_id.receiver_phone}
            from_email = 'yang_123456202204@163.com'
            to_email = receiver_mail
            result = mail.send_mail(subject, message, from_email, [to_email])
            print('result>>', result)
            return Response({'code': 200, 'data': result})
        except:
            error = traceback.format_exc()
            print('11111111111', error)
            return Response({'code': 406})
