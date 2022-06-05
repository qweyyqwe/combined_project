from django.db import models
from django.utils import timezone
from account.models import Account
# Create your models here.


# 公告表
class Announcement(models.Model):
    name = models.CharField(max_length=30, verbose_name="发布人")
    title = models.CharField(max_length=30, verbose_name="标题")
    be_time = models.DateTimeField(default=timezone.now, verbose_name='公告发布时间')
    content = models.CharField(max_length=168, verbose_name='公告内容')
    # 1未审核    2审核通过
    status = models.IntegerField(verbose_name="状态")
    fail_reason = models.CharField(max_length=168, verbose_name="未通过原因", null=True)

    class Meta:
        db_table = 'announcement_announcement'

    def __str__(self):
        return self.name


"""
class AuditingRecord0(models.Model):
    auditing_id = models.ManyToManyField(Account, verbose_name='审核人id')
    auditing_announcement = models.ManyToManyField(Announcement, verbose_name='公告id')
    auditing_time = models.DateTimeField(default=timezone.now, verbose_name='公告发布时间')
    fail_reason = models.CharField(max_length=168, verbose_name="未通过原因", null=True)
    # 0未审核    1审核通过     2审核不通过
    status = models.IntegerField(default=0, verbose_name="状态")

    class Meta:
        db_table = 'announcement_record0'


class AuditingRecord1(models.Model):
    auditing_id = models.ManyToManyField(Account)
    auditing_announcement = models.ManyToManyField(Announcement)
    # auditing_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    # auditing_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    auditing_time = models.DateTimeField(default=timezone.now, verbose_name='公告发布时间')
    fail_reason = models.CharField(max_length=168, verbose_name="未通过原因", null=True)
    # 0未审核    1审核通过     2审核不通过
    status = models.IntegerField(default=0, verbose_name="状态")

    class Meta:
        db_table = 'announcement_record1'
"""







