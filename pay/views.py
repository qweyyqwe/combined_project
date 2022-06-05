from django.shortcuts import render

# Create your views here.
import datetime
import time
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from good.models import Record
from pay.models import Order
from alipay import AliPay, AliPayConfig
from django.shortcuts import redirect

# 读到公钥私钥
app_private_key_string = open("utils/keys/private_key.txt").read()
alipay_public_key_string = open("utils/keys/public_key.txt").read()

# 生成订单
# 生成订单号
def create_order(order_id):
    # order = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(order_id) + str(random.randint(1000, 9999)))
    order = str(order_id) + str(random.randint(1000, 9999)) + str(int(time.time()))
    return order


# 生成订单
# 根据 出入的id
class CreateOrder(APIView):
    def post(self, request):
        record_id = request.data.get('order_id')
        record = Record.objects.filter(id=record_id).first()
        print(record)
        if not record:
            return Response({'msg': '没有该出入单', 'code': 500})
        # 生成订单号
        order_id = create_order(record_id)
        # print('22222222222222', order_id)
        order = Order.objects.create(order_code=order_id, record=record)
        # order = Order.objects.create(order_code=order_id, car_count=car, total_pay=money, record=record)    # TODO 这里报错
        order.save()
        return Response({'msg': '订单已生成', 'code': '200', 'order': order_id})


import random
from utils.keys.alipay import get_ali_object
from pay.models import Order
class Good(APIView):
    # def get_alipay_obj(self):
    #     """生成支付宝的客户端"""
    #
    # # 4. 创建支付宝实例
    # alipay = AliPay(
    #     appid='2021000119687640',
    #     app_notify_url=None,  # 默认回调url
    #     app_private_key_string=app_private_key_string,
    #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #     alipay_public_key_string=alipay_public_key_string,
    #     sign_type="RSA2",  # RSA 或者 RSA2
    #     debug=True,  # 默认False
    #     config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
    # )


    def post(self, request):
        try:
            order = request.data.get('order_id')
            print(order)
            order_id = Order.objects.get(id=order)
            print(type(order_id))
            print(order_id)
            print('>>>', order_id.order_code)
            # # TODO 调用get_ali_object()方法
            alipay = get_ali_object()
            # 生成支付的url
            query_params = alipay.direct_pay(
                subject="停车费",  # 商品简单描述
                out_trade_no=order_id.order_code,  # 用户购买的商品订单号（每次不一样） 20180301073422891
                total_amount=100,  # 交易金额(单位: 元 保留俩位小数)
            )
            pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
            return Response({'pay_url': pay_url, 'code': 200})
        except:
            error = traceback.format_exc()
            print(error)
            return Response({'msg': error, 'code': 406})
        # order_id = request.data.get('order_id')
        # print(order_id)
        # order = Order.objects.filter(record_id=order_id).first()
        #
        # if not order:
        #     return Response({'msg': '订单不存在', 'code': 500})
        # order = Order.objects.get(record_id=order_id)
        # # print(order)
        # order_code = order.order_code
        # print(order_code)
        # # 从记录表获取价格
        # record = Record.objects.filter(id=order_id).first()
        # money = record.money
        # # print(money)
        # # print('1111111111', order_code)
        # # print('222222222', money)
        # # 订单的生成时间       模型类默认有开始时间
        # '''
        #         # TODO 调用get_ali_object()方法
        # alipay = get_ali_object()
        # # 生成支付的url
        # try:
        #     query_params = alipay.direct_pay(
        #         subject="停车费支付",  # 商品简单描述
        #         out_trade_no=order_code,  # 用户购买的商品订单号（每次不一样） 20180301073422891
        #         total_amount=int(money),  # 交易金额(单位: 元 保留俩位小数)
        #     )
        #     # print(query_params)
        #     pay_url = "https://openapi.alipaydev.com/gteway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
        #     return Response({'pay_url': pay_url, 'code': 200})
        # except:
        #     error = traceback.format_exc()
        #     return error
        # '''
        # self.get_alipay_obj()
        # # try:
        # order_string = self.alipay.api_alipay_trade_page_pay(
        #     subject="停车场消费",  # 付款标题信息
        #     out_trade_no="%s" % order,  # 订单号  注意，标准的json格式没有 '' 单引号，只有 "" 双引号，python默认为 '' 单引号
        #     total_amount=money,  # 订单价格
        # )
        # self._gateway = "https://openapi.alipaydev.com/gateway.do"
        # print(order_string)
        # request_url = self._gateway + '?' + order_string
        # print(request_url)
        # # 把支付链接返给前端
        # print(request_url)
        # return Response({"msg": '请求成功，跳转支付页面', 'data': request_url, 'code': 200})
        # # except:
        # #     error = traceback.format_exc()
        # #     print('Alipay error:{}'.format(error))
        # #     print(error)
        # #     return Response({'msg': '请求失败', 'code': 500})
        #
        #
        # # 5. 调用支付宝的支付方法
        # # 如果你是 Python 3的用户，使用默认的字符串即可
        # subject = "多多商城测试订单"
        #
        # # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # # https://openapi.alipay.com/gateway.do 这个是线上的
        # # 'https://openapi.alipaydev.com/gateway.do' 这个是沙箱的
        # order_string = alipay.api_alipay_trade_page_pay(
        #     out_trade_no=order_id,
        #     total_amount=str(order.total_amount),  # 一定要进行类型转换,因为decimal不是基本数据类型
        #     subject=subject,
        #     return_url=settings.ALIPAY_RETURN_URL,  # 支付成功之后,跳转的页面
        #     notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
        # )
        # # 6.  拼接连接
        # pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        # return JsonResponse({'code': 0, 'errmsg': 'ok', 'alipay_url': pay_url})




# 回调
class Hui(APIView):
    def get(self, request):
        print('回调接口11111111111111')
        out_trade_no = request.data.get("out_trad6e_no")
        trade_no = request.data.get("trade_no")

        print("order_no和订单流水号", out_trade_no, trade_no)
        resp = Order.objects.get(id=out_trade_no)
        print(resp.status)
        if resp.status == 2:
            return Response({"code": 200, "message": "您已支付过了"})

        resp.status = 2
        resp.save()
        # else:
        #     sql = "update orders set status = 2,dingdan_id='%s' where code='%s'" % (trade_no, out_trade_no)
        #     db1.update(sql)
        #     db1.commit()
        # return redirect("http://127.0.0.1:8080/")
        return redirect("http://127.0.0.1:8080/")



        # 3. 读取应用私钥和支付宝公钥

        # app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        # alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()




        # 7. 返回响应



# class GetAliPay(APIView):
#     """查询支付接口"""
#     def get_pay_result(self, order):
#         self.alipay = AliPay(
#             appid="2021000118696349",
#             app_notify_url=None,  # 默认回调url
#             app_private_key_string=app_private_key_string,
#             alipay_public_key_string=alipay_public_key_string,
#             # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#             sign_type="RSA2",  # RSA 或者 RSA2
#             debug=True  # 默认False
#         )
#         # 此为支付宝交易查询接口
#         response = self.alipay.api_alipay_trade_query(trade_no=order, out_trade_no=False)
#         return response
#
#     def get(self, request):
#         order_id = request.data.get('order_id')
#         order = Order.objects.get(order_id=order_id)
#         if not order or order.status != 0:
#             return Response({'msg': '订单不存在或者已付款或者未付款', 'code': 500})
#         response = self.alipay.api_alipay_trade_query(order_id)
#         print('111111111111', response)
#         order.status = 2
#         order.save()
#         return Response({'msg': "购买成功",'code':200})