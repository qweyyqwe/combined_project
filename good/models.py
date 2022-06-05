from django.db import models
from django.utils import timezone


# Create your models here.


class User(models.Model):
    """用户表"""
    name = models.CharField(max_length=30, verbose_name="车主名称")
    car_number = models.CharField(max_length=30, verbose_name="车牌号", unique=True)
    type = models.IntegerField(default=2, verbose_name="1包月 2非包月")

    class Meta:
        db_table = 'owner_user'


class TypeMoney(models.Model):
    """类型表"""
    type = models.IntegerField(default=1, verbose_name='1包月 2业主 3非业主')
    money = models.DecimalField(max_length=10, decimal_places=2, max_digits=5, verbose_name='每小时单价')
    # money = models.FloatField(verbose_name='每小时单价')

    class Meta:
        db_table = 'owner_type_money'


class Record(models.Model):
    """出入记录"""
    car = models.CharField(max_length=30, verbose_name="车牌号")
    in_time = models.DateTimeField(default=timezone.now, verbose_name='进来的时间')
    out_time = models.DateTimeField(verbose_name='离开的时间', blank=True, null=True)
    # out_time = models.DateTimeField(verbose_name='离开的时间')
    money = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="价格", blank=True, null=True)

    class Meta:
        db_table = 'owner_record'

    def to_json(self):
        return {
            'id': self.id,
            'car': self.car,
            'in_time': str(self.in_time.strftime('%Y-%m-%d %H:%M:%S') if self.in_time else '-'),
            'out_time': str(self.out_time.strftime('%Y-%m-%d %H:%M:%S') if self.out_time else '-'),
            'money': str(self.money if self.money else '-')

        }
