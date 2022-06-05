from django.db import models
from django.utils import timezone
# Create your models here.
from good.models import Record


class Order(models.Model):
    """
    支付订单表
    """
    order_code = models.CharField(max_length=20, verbose_name='订单唯一标识')
    car_count = models.CharField(max_length=20, verbose_name='车牌号', blank=True, null=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='订单生成时间')
    done_time = models.DateTimeField(verbose_name='订单付款时间', blank=True, null=True)
    status = models.IntegerField(default=0, verbose_name='订单的支付状态')     # 0未支付，1支付中，2完成支付，3支付异常，4支付取消
    # total_pay = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='实际支付金额')
    total_pay = models.IntegerField(verbose_name='实际支付金额', blank=True, null=True)

    class Meta:
        """重命名"""
        db_table = 'pay_order'

