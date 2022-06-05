# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : public.py
# @Software: PyCharm
# 公共方法

import random
import time


# 无限级分类重组
def xtree(data):
    if len(data) <= 0:
        return data
        # 对数据解析重组
    tree = {}
    for i in data:
        # print('1111', i)
        i['label'] = i['name_menu']
        tree[i['id']] = i

    # 初始化列表
    dlist = []
    for j in data:
        # 查看pid是否为0，为0代表第一级
        pid = j['pid']
        if pid == 0:
            dlist.append(j)
        else:
            # 判断此子类的父类下面是否已经有子类，如果没有初始化
            if 'children' not in tree[pid]:
                tree[pid]['children'] = []
            tree[pid]['children'].append(j)
    return dlist


# 用户可访问
def user_tree(data):
    if len(data) <= 0:
        return data
        # 对数据解析重组
    tree = {}
    for i in data:
        # print('1111', i)
        i['label'] = i['name_menu']
        tree[i['id']] = i

    # 初始化列表
    dlist = []
    for j in data:
        # 查看pid是否为0，为0代表第一级
        pid = j['pid']
        if pid == 0:
            dlist.append(j)
        else:
            # 判断此子类的父类下面是否已经有子类，如果没有初始化
            if 'children' not in tree[pid]:
                tree[pid]['children'] = []
            tree[pid]['children'].append(j)
    return dlist


def create_order(order_id):
    order = str(order_id) + str(random.randint(1000, 9999)) + str(int(time.time()))
    return order
