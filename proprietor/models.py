from django.db import models

# Create your models here.

from account.models import Account
from django.utils import timezone


class Area(models.Model):
    name = models.CharField(max_length=15, verbose_name='区域名称', default="")
    money = models.DecimalField(max_length=10, decimal_places=2, max_digits=5, verbose_name='每平方/钱')

    class Meta:
        db_table = 'proprietor_area'

    def __str__(self):
        return self.name


class House(models.Model):
    floor = models.IntegerField(verbose_name="楼层号")
    unit = models.IntegerField(verbose_name="单元号")
    house = models.IntegerField(verbose_name="房屋号")
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='区域id')
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='业主id')
    square = models.DecimalField(max_length=10, decimal_places=2, max_digits=5, verbose_name='平方米')

    class Meta:
        db_table = 'proprietor_house'

    def __str__(self):
        return str(self.square)


class RepairInto(models.Model):
    content = models.CharField(max_length=168, verbose_name="故障原因")
    # 0未修复 / 1处理中 / 2未解决/ 3完成
    status = models.IntegerField(default=0, verbose_name="状态")
    house_id = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="房屋id")
    code = models.CharField(max_length=40, verbose_name="唯一标识", unique=True)
    account_repair_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="维修人员id", null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name="报修人的手机号", null=True)
    repair_man = models.CharField(max_length=30, verbose_name="报修人名字", default="")
    img = models.CharField(max_length=268, verbose_name="故障图片url")
    be_time = models.DateTimeField(default=timezone.now, verbose_name='报修时间')

    class Meta:
        db_table = 'proprietor_repairinto'


class 







