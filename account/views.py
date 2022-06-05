# Create your views here.

# import 导包

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
from django.contrib.auth.hashers import make_password, check_password

# 本地导包
from utils.jwt import jwt_token
from account.models import Account, UserGroup
from .models import Resource, Menu
from .serializers import ResourceSer, MenuSer
from utils.public import xtree
from utils.account_login import get_resource_list, menu_left_list
from utils.redis_cache import mredis


# 注册
class Register(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not all([username, password]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        name_count = Account.objects.filter(username=username).count()
        if name_count > 0:
            return Response({'code': 400, 'mes': '该用户已被注册'})
        # secret = make_password(password)
        account = Account.objects.create_user(username=username, password=password)
        return Response({'code': 200, 'meg': '注册成功'})


# 登录
class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        if not all([username, password]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        user_name = Account.objects.filter(username=username).first()
        if not user_name:
            return Response({'msg': '用户名不存在', "code": 400})
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(user)
                    resource_list = get_resource_list(user)
                    token = jwt_token.encode_token({"username": username})
                    # data = jwt_payload_handler(username)
                    # token = jwt_encode_handler(data)
                    return Response({"code": 200, "msg": "登录成功", 'username': user.username, 'token': token,
                                     'resource': resource_list})
                return Response({'code': 400, 'msg': '什么错误'})
            return Response({'code': 406, 'msg': '密码账号错误'})
        except:
            error = traceback.format_exc()
            print('2222222', error)
            return Response({'code': 406, 'msg': error})


# select r.id,r.name_resource,r.url,rr.id as pid,rr.name_resource as name from account_roles_resource as
# acc_ro_re  left join account_resource as r on acc_ro_re.resource_id=r.id inner join account_resource
# as rr on r.pid=rr.id where acc_ro_re.roles_id=1;
# +------+---------------+--------------+-----+----------+
# | id   | name_resource | url          | pid | name     |
# +------+---------------+--------------+-----+----------+
# |    4 | 寄快递        | /add_express |   3 | 快递服务 |
# +------+---------------+--------------+-----+----------+


class GetUserRolesList(APIView):
    """
    权限
    """
    serializer_class = ResourceSer

    # parmisson_class = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.query_params.get('username')
        users = Account.objects.filter(username=user).first()
        resource_list = get_resource_list(users)
        print(resource_list)
        menu_list = menu_left_list(resource_list)
        print(menu_list)
        return Response({'code': 200, 'data': menu_list})

        # role_id = request.data.get('role_id')
        # sql = "select r.id,r.name,r.url,rr.id as pid,rr.name as pname from role_resource as ro_re  left join resource as " \
        #       "r on ro_re.resource_id=r.id inner join resource as rr on r.pid=rr.id where ro_re.role_id= %d" % int(role_id)
        # data = db1.findAll(sql)
        # res = menu(data)
        # return jsonify({'code': 200, 'user_list': res})


class GetMenuList(APIView):
    """
    获取无限级分类
    """

    def get(self, request):
        menu = cache.get('menu_list', None)
        if not menu:
            menu_list = Menu.objects.filter(status=1)
            menu_list = MenuSer(menu_list, many=True).data
            menu = xtree(menu_list)
            # cache.set('menu_list', menu, 60*10)
        return Response({'code': 200, 'data': menu})


class AddMenu(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        pid = data.get('pid')
        status = data.get('status')
        print(name, pid)
        if not all([name, pid]):
            return Response({'msg': '信息不全，请补全', "code": 400})
        menuname_count = Menu.objects.filter(name_menu=name).count()
        if menuname_count > 0:
            return Response({'code': 406, 'msg': '该名称已存在'})
        # pid_count = Menu.objects.filter(pid=pid)
        pid_count = Menu.objects.filter(id=pid).count()
        if pid_count == 0:
            return Response({'msg': '该类别的父类id不存在', 'code': 500})
        menu = Menu.objects.create(name_menu=name, pid=pid, status=status)
        menu.save()
        # print('pid>>>>>>', pid_count)
        return Response({'code': 200, 'msg': '添加成功'})


class PutMenu(APIView):
    """
    修改菜单
    """

    def post(self, request):
        id = request.data.get('id')
        name = request.data.get('name')
        print(id, name)
        if not all([name, id]):
            return Response({'msg': '信息不可为空，请补全', 'code': 500})
        menu = Menu.objects.filter(id=id).first()
        if not menu:
            return Response({'msg': '该菜单不存在', 'code': 500})
        name_num = Menu.objects.filter(name_menu=name).count()
        if name_num > 0:
            return Response({'msg': '该菜单名称已存在', 'code': 500})
        menu.name_menu = name
        menu.save()
        return Response({'msg': '修改成功', 'code': 200})


class DeleteMenu(APIView):
    """
    删除
    """

    def post(self, request):
        id = request.data.get('id')
        menu = Menu.objects.filter(id=id).first()
        if not menu:
            return Response({'msg': "没有该菜单id,请输入正确的id", 'code': 500})
        menu = Menu.objects.filter(Q(id=id) & Q(status=0)).count()
        if menu == 1:
            return Response({'code': 406, 'msg': '没有该菜单或已删除'})
        menu = Menu.objects.filter(id=id).update(status=0)
        return Response({'msg': "删除成功", 'code': 200})


# 注册邮箱
class AddEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        pass


class Image(APIView):
    def get(self, uuid):
        """
        request:
        :return: image/jpg
        :param request:
        :param uuid:  通用唯一识别符,用于标识唯一图片验证码属于哪个用户的
        """

        '''
                # 生成图片验证码
        text, image = captcha.generate_captcha()
        # print(text, image)

        # 保存图像验证码,保存到redis
        redis_conn = get_redis_connection('verify_code')

        # name time value
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 响应图形验证码
        return HttpResponse(image, content_type='image/png')
        '''

        # 路由传参
        # 调用captch外部库生成图片和验证码
        name, text, img = captcha.generate_captcha()
        # 3.2、把验证码写入redis(以uuid作为key)
        # get_redis_connection函数：功能是获取redis链接对象，参数是一个字符串(是django缓存配置名称)
        # 返回值是一个redis链接对象
        conn = get_redis_connection('verify_code')
        print(conn)
        # Redis < ConnectionPool < Connection < host = 127.0.0 .1, port = 6379, db = 2 >> >
        # setex img_37728d6c-e219-44c5-8f81-4245a9e557a4 300 KJHG
        conn.setex('img_%s' % uuid, 60 * 3, text)
        # 4、构建响应(返回图片数据)
        # 构造的响应体数据是图片的二进制字节数据，需要设置响应头Content-Type:image/jpeg，来
        # 告诉浏览器响应体数据是图片数据，这样浏览器才能够渲染图片
        return HttpResponse(img, content_type='image/png')


# from django.core.mail import send_mail

# def test_email():
#     send_mail(subject='测试邮件——修改密码',
#               # message="点击次<a href='https://www.baidu.com/'>点我进百度</a>链接进行修改",
#               message='''
#               <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
# <li>
#     <ll>你</ll>
# </li>
# <li>
#     <ll>好</ll>
# </li>
# <li>
#     <ll>！</ll>
# </li>
# <li>
#     <ll>OK</ll>
# </li>
# <li>
#     <ll>？</ll>
# </li>
#
# </body>
# </html>
#               ''',
#               from_email='yang_123456202204@163.com', recipient_list=['3413299451@qq.com'])
#     # 刘洋——a1919893434@163.com
#
#     return HttpResponse('发送成功')


# class Email(APIView):
#     def get(self, request):
#         test_email()
#         return Response({'code': 200})


class EmailSong(APIView):
    def post(self, request):
        subject = '测试邮件主题'
        context = {}
        from_email = '491061108@qq.com'  # 邮件发送人
        recipient_list = ['2837379503@qq.com', '18332782513@163.com']  # 邮件接收人

        # 这里需要提前写好html的页面
        email_template_name = 'template.html'
        t = loader.get_template(email_template_name)  # 导入模板

        html_content = t.render(context)  # 模板参数
        msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()  # 发送邮件

        return Response({'code': 200})


# 通过邮箱修改密码
"""
该用户是否有邮箱  没有则注册

后端获取到前端的账号， 
生成url   http://lo + code + email  一个路由 邮箱发送url

获取修改后的密码

"""



class GetPutPassword(APIView):
    def post(self, request):
        # phone = request.data.get('phone')
        # name = Account.objects.get(phone=phone)
        # print(name)
        # print(type(name))
        # list = model_to_dict(name)
        # print(email)
        account = request.data.get('phone_email')
        name = Account.objects.filter(phone=account).first()
        email = name.email
        print(account, email)
        if email is None:
            return Response({'code': 406, 'msg': '该用户未注册邮箱，请注册'})
        # if re.match(r'/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/', email):
        #     return Response({'code': 400, 'message': '邮箱格式错误'})
        try:
            code = uuid.uuid1().hex
            mredis.setex_str(code, 3600, email)
            subject = '修改密码'
            message = "点击次<a href='http://localhost:8000/account/get_password?code={}'>修改</a>链接进行修改".format(code)
            from_email = [email]
            recipient_list = ['3413299451@qq.com']
            send_mail(subject, message, from_email, recipient_list)
            return Response({'code': 200, 'message': "邮件成功发送"})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'code': 10011, 'message': '发送邮件失败'})


class PutPassword(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        code_undo = mredis.str_get(code)
        if code_undo is not None:
            # 跳转到修改密码页面
            url = 'http://localhost:8080/email_pass?code={}'.format(code_undo.decode())
            print(url)
            return redirect(url)
        else:
            return Response({'code': 400, 'message': '验证失败，请重新操作'})


from django.forms.models import model_to_dict
class Validate(APIView):
    def post(self, request):
        email = request.data.get('phone_email')
        password = request.data.get('password')
        paw = make_password(password)

        try:
            print(email)
            print(paw)
            user = Account.objects.get(email=email)
            user.password = paw
            user.save()
            return Response({'code': 200, 'msg': '修改成功'})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'code': 500, 'msg': '错误失败'})


# express_status = MailRecord.objects.get(id=express)
#         express_status.status = 1
#         express_status.save()

