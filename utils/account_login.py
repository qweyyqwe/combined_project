# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : account.py
# @Software: PyCharm


from functools import wraps
from rest_framework.permissions import BasePermission
from account.models import UserGroup, Resource
from account.serializers import UserGroupSer, ResourceSer


def login_required(func):
    """强制登录装饰器"""
    # wraps 是返回装饰器,参数是传来的函数,
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("func的名字是>>", func.__name__)
        if g.user_id is not None:
            return func(*args, **kwargs)
        return {'code': 401, 'message': '无效token 账号为空'}
    return wrapper


def superuser(func):
    """
    权限验证装饰器

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if list(set(g.role_id) & set(list([2, 3]))):
            return func(*args, **kwargs)
        return {'code': 403, 'message': 'Not permission'}
    return wrapper


# 自定义权限
class CustomAuthority(BasePermission):
    def has_params(self, request, view):
        user = request.user
        return True or False


def get_resource_list(user):
    # print('方法1')
    group_list = UserGroup.objects.filter(user=user)
    # print('>>>>>>>>>>>>..', group_list)
    resource_list = []
    for group in group_list:
        # print(dir(group))
        resource = ResourceSer(group.resource.all(), many=True).data
        # print(resource)
        for data in resource:
            resource_list.append(data)
            # print("data?>>>>>>>>", data)
    return resource_list


# """获取用户资源列表"""
# def get_resource_list(user):
#     group_list = UserGroup.objects.filter(user=user)
#     print('>>>>>>>>>>>>>>>>>>>', group_list)
#     resource_list = []
#     for group in group_list:
#         # print(dir(group))
#         resource = ResourceSer(group.resource.all(), many=True)
#         print(resource)
#         for data in resource:
#             print("data?>>>>>>>>", data)
#             resource_list.append(data)
#     return resource_list


# 左侧导航栏重组
# def menu_left_list(data):
#     print(data)
#     if len(data) <= 0:
#         return data
#     list1 = []  # 整条数据存放
#     idlist = []   # 去重使用
#     # 遍历拿出菜单
#     for i in data:
#         print('第一>>>>>>>>iiii', i)
#         if i['pid'] not in idlist:
#             print('没第一走一一iiiiiiiiii>>>>>>>>>>>>>>>', i)
#             list1.append({'id': i['pid'], 'name': i['resourcename'], 'son': []})
#             idlist.append(i['pid'])
#             print('二二111111111>>>', list1)
#             print('三三2222222222', idlist)
#     # 把资源放入列表
#     for index, item in enumerate(list1):
#         for j in data:
#             print('>>>>>>>>>>>jjj', j)
#             if item['id'] == j['pid']:
#                 list1[index]['son'].append(j)
#     return list1
def menu_left_list(data):
    if len(data) <= 0:
        return data
    tree = {}
    for i in data:
        # 数的第一条数据就 变成data中i循环的第一条数据
        tree[i['id']] = i
    dlist = []
    for j in data:
        # 查看pid 是不是0，0为一级标签
        #  j['pid'] 就是data 数据中  每循环一条的数据中的pid
        pid = j['pid']
        if pid == 0:
            dlist.append(j)
        else:
            # 判断此子类的父类下面是否已经有了子类
            # 如果没有得到这pid 就跳出本次循环进入下一次循环
            if not tree.get(pid, None):
                continue
            # 如果son不在tree[pid]里面
            #    则就添加一个空列表
            # 否则就是在添加son一条数据
            if 'son' not in tree[pid]:
                tree[pid]['son'] = []
            tree[pid]['son'].append(j)
    return dlist

