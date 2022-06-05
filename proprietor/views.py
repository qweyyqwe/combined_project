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
from django.forms.models import model_to_dict
from django.db import transaction

# 本地导包
from utils.public import xtree
from utils.redis_cache import mredis
from .models import Area, House, RepairInto
from account.models import Account
from .serializers import RepairIntoSer
from utils.public import create_order
from account.serializers import AccountSer


# 添加区域
class AddArea(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        name = data.get('name')
        money = data.get('money')
        if not all([name, money]):
            return Response({'code': 406, 'msg': '信息不可为空'})
        house, _ = Area.objects.get_or_create(name=name, money=money)
        print('11111', house)
        house.save()
        data = model_to_dict(house)
        return Response({'code': 200, 'msg': '添加区域成功', 'data': data})


class PutArea(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        id = data.get('id')
        name = data.get('name')
        money = data.get('money')
        if not all([name, money]):
            return Response({'code': 406, 'msg': '信息不可为空'})
        area = Area.objects.get(id=id)
        area.name = name
        area.money = money
        area.save()
        return Response({'code': 200, 'msg': '区域数据修改成功', 'data': data})


# 完善房屋信息
class AddHouse(APIView):
    def post(self, request):
        try:
            data = request.data
            floor = data.get('floor')
            unit = data.get('unit')
            house = data.get('house')
            area_id = data.get('area_id')
            square = data.get('square')
            account_id = data.get('user_id')
            if not all([floor, unit, house, square]):
                return Response({'code': 406, 'msg': '信息不可为空'})
            area = Area.objects.filter(id=area_id).count()
            if area == 0:
                return Response({'code': 500, 'msg': '该房屋不存在'})
            account = Account.objects.filter(Q(id=account_id) & Q(is_staff=0)).count()
            if account == 0:
                return Response({'code': 500, 'msg': '该用户不存在'})
            houses, _ = House.objects.get_or_create(floor=floor, unit=unit, house=house, square=square,
                                                    area_id_id=area_id, account_id_id=account_id)
            print('222222', houses)  # TODO 30????
            # house.area_id_id = area_id
            # house.account_id_id = account_id
            houses.save()
            data = model_to_dict(houses)
            return Response({'code': 200, 'msg': '已完善房屋信息', 'data': data})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'code': 400, 'msg': error})


class PutHouse(APIView):
    def post(self, request):
        data = request.data
        id = data.get('id')
        floor = data.get('floor')
        unit = data.get('unit')
        house = data.get('house')
        area_id = data.get('area_id')
        square = data.get('square')
        account_id = data.get('user_id')
        if not all([floor, unit, house, square]):
            return Response({'code': 406, 'msg': '信息不可为空'})
        area = Area.objects.filter(id=area_id).count()
        if area == 0:
            return Response({'code': 500, 'msg': '该房屋不存在'})
        account = Account.objects.filter(Q(id=account_id) & Q(is_staff=0)).count()
        if account == 0:
            return Response({'code': 500, 'msg': '该用户不存在'})
        house_put = House.objects.get(id=id)
        house_put.floor = floor
        house_put.unit = unit
        house_put.house = house
        house_put.area_id = area_id
        house_put.square = square
        house_put.account_id = account_id
        house_put.save()
        return Response({'code': 200, 'msg': '房屋数据修改成功'})


# 添加报修内容
class AddRepairInto(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        data = request.data
        content = data.get('content')
        phone = data.get('phone')
        img = data.get('img')
        repair_man = data.get('repair_man')

        build_no = data.get('build_no')
        unit_no = data.get('unit_no')
        house_no = data.get('house_no')
        print(data)
        try:
            house = House.objects.filter(Q(floor=build_no) & Q(unit=unit_no) & Q(house=house_no)).first()
            print(house)
            # print('house_id>>>>', house_id)
            house_id = house.id
            code = create_order(house_id)
            print(code)
            # # 显式的开启一个事务
            # with transaction.atomic():
            #     # 创建事务保存点
            #     save_id = transaction.savepoint()
            area = House.objects.filter(id=house_id).count()
            if area == 0:
                return Response({'code': 500, 'msg': '该房屋不存在'})
            # # 出错就回滚
            # transaction.savepoint_rollback(save_id)
            repair, _ = RepairInto.objects.get_or_create(content=content, phone=phone, img=img,
                                                         repair_man=repair_man,
                                                         house_id_id=house_id, code=code, status=0)
            repair.save()
            mredis.r_push('repair', code)
            data = model_to_dict(repair)
            # # 提交订单成功，显式的提交一次事务
            # transaction.savepoint_commit(save_id)
            return Response({'code': 200, 'msg': '上传报修', 'data': data})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'code': 400, 'msg': error})


# class UpdateRepairInto(APIView):
#     def post(self, request):

from celery_task.tasks import test,send_email2
class Get(APIView):
    def get(self,request):
        name = test(1,1)
        return Response({"name":name})




def set_audit(auditid):
    count = mredis.t_len('repair')
    if count > 0:
        print('1111111111111')
        code = mredis.r_pop('repair').decode()
        print(code)
        repairinto = RepairInto.objects.filter(Q(status=0) & Q(code=code))[0]
        print(repairinto)
        repairinto.account_repair_id_id = int(auditid)
        repairinto.save()


class AllotRepair(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pepair_list = []
        user_repair_man = Account.objects.filter(status=2).all()
        for i in user_repair_man:
            pepair_list.append(i.id)
        print(pepair_list)
        while True:
            for i in pepair_list:
                set_audit(i)


# 维修员查看自己的
class MaintainerList(APIView):
    def get(self, request):
        # 通过名字获取到角色
        repair_id = 6
        repair = RepairInto.objects.filter(Q(status=0) & Q(account_repair_id_id=repair_id)).all()
        repair_ser = RepairIntoSer(repair, many=True)
        return Response({'code': 200, 'repair_list': repair_ser.data})


class MaintainerWork(APIView):
    def post(self, request):
        # repair_into_id = request.data.get('repair_id')
        repair_into_id = 55
        print('>>>>>>', repair_into_id)
        repair_id = RepairInto.objects.get(id=repair_into_id)
        print(type(repair_id))
        repair_id.status = 1
        repair_id.save()
        return Response({'code': 200, 'msg': '正在维修'})


class MaintainerNoWork(APIView):
    def post(self, request):
        # repair_into_id = request.data.get('repair_id')
        repair_into_id = 56
        print('>>>>>>', repair_into_id)
        repair_id = RepairInto.objects.get(id=repair_into_id)
        print(type(repair_id))
        repair_id.status = 2
        if repair_id.status == 2:
            return Response({'code': 406, 'msg': '未完成'})
        repair_id.save()
        return Response({'code': 200, 'msg': '未修复'})


class MaintainerOutWork(APIView):
    def post(self, request):
        # repair_into_id = request.data.get('repair_id')
        repair_into_id = 56
        print('>>>>>>', repair_into_id)
        repair_id = RepairInto.objects.get(id=repair_into_id)
        print(type(repair_id))
        repair_id.status = 3
        repair_id.save()
        return Response({'code': 200, 'msg': '维修成功'})


# 用户登录
class ShowUser(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        repair = RepairInto.objects.filter(Q(status=0) & Q(id=user_id)).all()
        repair_ser = RepairIntoSer(repair, many=True)
        return Response({'code': 200, 'repair_list': repair_ser.data})


# 管理员登录
class ShowSuperuser(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        if user_id.is_superuser==1:

            repair = RepairInto.objects.all()
            repair_ser = RepairIntoSer(repair, many=True)
            return Response({'code': 200, 'repair_list': repair_ser.data})
        else:
            return Response({'code': 401, 'msg': '权限不足'})


# 点击直接缴费成功
class PayMoney(APIView):
    def post(self, request):
