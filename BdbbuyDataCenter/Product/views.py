from django.shortcuts import render


from .models import *

# django
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_http_methods(["GET"])
def get_out_of_date_product(request):
    params = {}
    # 参数获取
    # 按库存数查找的参数
    low_count = request.GET.get('lowCount', None)
    # 查找过期商品
    out_of_date = request.GET.get('outOfDate', False)
    # 按一段时间销量查找数据
    order_day = request.GET.get('orderDay', None)

    # 获取商品数据
    if low_count:
        params['low_count'] = low_count

    if out_of_date == 'true':
        params['out_of_date'] =True

    if order_day:
        params['order_day'] = order_day

    product_list = Product.get_lowcount_outofdate_products(**params)
    return JsonResponse({'data': {'order_list': product_list, 'totalCount': len(product_list)}})