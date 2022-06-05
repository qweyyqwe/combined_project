"""
支付相关模型
"""

from django.db import models
from django.utils import timezone


class Driver(models.Model):
    """
    司机表
    """
    name = models.CharField(max_length=10, verbose_name='司机名')
    phone = models.CharField(max_length=11, verbose_name='司机手机号')
    status = models.IntegerField(verbose_name='司机状态0空闲1繁忙', default=0)

    class Meta:
        db_table = 'logistics_driver'


class Truck(models.Model):
    """
    货车表
    """
    plate_number = models.CharField(max_length=10, verbose_name='车牌号')
    status = models.IntegerField(verbose_name='状态0空闲1繁忙', default=0)

    class Meta:
        db_table = 'logistics_truck'


class MailRecord(models.Model):
    """
    快递记录表

    发货单号、商品名称、数量、时间、发件人、收货人、收货地址、发货地址、物流状态
                、快递价格、收货电话、运货车辆、运货司机
    """
    order_code = models.CharField(max_length=20, verbose_name='快递单号', unique=True)
    name = models.CharField(max_length=10, verbose_name='商品名称')
    # count = models.IntegerField(default=1, verbose_name='商品数量')
    sender = models.CharField(max_length=20, verbose_name='发件人')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    send_time = models.DateTimeField(default=timezone.now, verbose_name='发货时间')
    to_place = models.CharField(max_length=50, verbose_name='收货地址', null=True)
    from_place = models.CharField(max_length=50, verbose_name='发货地址', null=True)
    # depart = models.ForeignKey('Site', on_delete=models.CASCADE, verbose_name='出发地')
    # goal = models.ForeignKey('Site', on_delete=models.CASCADE, verbose_name='目的地')
    # 快递状态 0 未发货 1 运输中 2 抵达     3用户签收
    status = models.IntegerField(default=0, verbose_name='快递状态')
    money = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="快递价格", blank=True, null=True)
    # sender_phone = models.CharField(max_length=13, verbose_name='发货人电话')
    receiver_phone = models.CharField(max_length=13, verbose_name='收货人电话')
    truck_id = models.ForeignKey(Truck, on_delete=models.CASCADE, verbose_name='货车信息')
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机信息')
    # desc = models.CharField(max_length=50, verbose_name='快递信息', default='')

    class Meta:
        db_table = 'logistics_record'


class Site(models.Model):
    """
    地址表
    """
    go_site = models.CharField(max_length=15, verbose_name='出发地')
    from_site = models.CharField(max_length=15, verbose_name='目的地')
    money = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="费用", blank=True, null=True)

    class Meta:
        db_table = 'logistics_site'


# # 记录表
# class RecordExpress(models.Model):
#     code = models.CharField(max_length=20, verbose_name='快递单号', unique=True)
#     money = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="快递价格", blank=True, null=True)
#     send_time = models.DateTimeField(default=timezone.now, verbose_name='时间')
#     sender = models.CharField(max_length=20, verbose_name='发件人')
#
#     class Meta:
#         db_table = 'logistics_record_express'
