# Create your models here.


"""
class Account(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    # roles = models.ManyToManyField(verbose_name='担任的角色', to='Roles', blank=True)

    class Meta:
        db_table = 'account_account'


# # 用户表
# class Account(models.Model):
#     username = models.CharField(max_length=20, verbose_name='用户名')
#     password = models.CharField(max_length=30, verbose_name='密码')
#     phone = models.CharField(max_length=11, verbose_name='手机号')
#     email = models.CharField(max_length=160, verbose_name='邮箱')
#     roles = models.ManyToManyField(verbose_name='担任的角色', to='Roles', blank=True)
#
#     class Meta:
#         db_table = 'account_account'


# 角色表
class Roles(models.Model):
    name_roles = models.CharField(max_length=20, verbose_name='角色名')
    user = models.ManyToManyField(Account, blank=True)
    # resource = models.ManyToManyField(verbose_name='拥有的所有权限', to='Resource', blank=True)

    class Meta:
        db_table = 'account_roles'


# 资源表
class Resource(models.Model):
    name_resource = models.CharField(max_length=20, verbose_name='资源名')
    url = models.CharField(max_length=20, verbose_name='url/路由')
    pid = models.IntegerField(verbose_name='子id')

    class Meta:
        db_table = 'account_resource'


"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True, null=True)
    # 0普通用户/1超级用户/2维修员
    status = models.IntegerField(default=0, verbose_name="用户等级")
    # is_staff/  0普通用户/1超级用户/2维修人员

    class Meta:
        db_table = 'account_account'

    def __str__(self):
        return self.username


# class Role(models.Model):
#     name = models.CharField(max_length=20, verbose_name='角色名', null=True)
#
#     class Meta:
#         db_table = 'account_roles'
#
#     def __str__(self):
#         return self.name


class Resource(models.Model):
    # role = models.ForeignKey(to='Role', on_delete=models.CASCADE)
    resourcename = models.CharField(max_length=30, verbose_name='名称', default='')
    url = models.CharField(max_length=256, verbose_name='角色资源地址', null=True)
    status = models.IntegerField(verbose_name='角色资源状态', default=1)
    pid = models.IntegerField(verbose_name='子id', default='')

    class Meta:
        db_table = 'account_resource'

    def __str__(self):
        return self.resourcename


# 用户组
class UserGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name='名称', default='')
    user = models.ManyToManyField(Account)
    resource = models.ManyToManyField(Resource)

    class Meta:
        db_table = 'account_usergroup'

    def __str__(self):
        return self.name


class Menu(models.Model):
    name_menu = models.CharField(max_length=30, verbose_name='名称', default='')
    pid = models.IntegerField(verbose_name='子id', default=0)
    status = models.IntegerField(verbose_name='状态0不可见/1可见', default=1)

    class Meta:
        db_table = 'account_menu'

    def __str__(self):
        return self.name_menu
