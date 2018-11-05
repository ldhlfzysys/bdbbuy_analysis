from django.shortcuts import render

import json
from datetime import datetime,timedelta
import time
# django

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# custom
from .models import *
from Other.models import Area



# Create your views here.

@require_http_methods(["GET"])
def get_order_list(request):
    default_from_date = datetime.now().replace(hour=0, minute=0, second=0)
    search_from_date = request.GET.get('fromDate', default_from_date)
    search_to_date = request.GET.get('toDate', datetime.now())

    timeArray1 = time.strptime(search_from_date, "%Y-%m-%d %H:%M:%S")
    timestamp1 = time.mktime(timeArray1)

    timeArray2 = time.strptime(search_to_date, "%Y-%m-%d %H:%M:%S")
    timestamp2 = time.mktime(timeArray2)

    delta_time = timestamp1 - (timestamp2 - timestamp1)
    time_local = time.localtime(delta_time)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    areas = request.GET.get('areaId', '')
    if areas == '':
        areas = 'all'
    order_list_q = []
    last_order_list_q = []
    all_area_order_list = Orders.objects.filter(create_at__gte=search_from_date, create_at__lte=search_to_date)
    last_order_list_q = Orders.objects.filter(create_at__gte=dt, create_at__lte=search_from_date)
    if areas.find('all') != -1:
        order_list_q = all_area_order_list
    else:
        area_list = areas.split('-')
        order_list_q = Orders.objects.filter(create_at__gte=search_from_date, create_at__lte=search_to_date, area_id__in=area_list)
        last_order_list_q = Orders.objects.filter(create_at__gte=dt, create_at__lte=search_from_date, area_id__in=area_list)
    all_order_list = [i.serializable_values() for i in order_list_q]
    validate_order_list = []
    sale_total = 0
    tax_total = 0
    refund_order = 0
    for order in all_order_list:
        if order['status'] != OrderStatus.OrderNotPay.value \
                and order['status'] != OrderStatus.OrderRefunded.value:
            # 有效订单
            sale_total += float(order['total'])
            tax_total += float(order['tax_total'])
            validate_order_list.append(order)

        if order['status'] == OrderStatus.OrderRefunded.value:
            refund_order += 1

    last_validate_order_list = []
    for order in last_order_list_q:
        if order.status != OrderStatus.OrderNotPay.value and order.status != OrderStatus.OrderRefunded.value:
            last_validate_order_list.append(order)

    area_order_info = {}
    for order in all_area_order_list:
        if area_order_info.get(order.area_id, None) == None:
            area_order_info[order.area_id] = (float(order.total), Area.objects.get(id=order.area_id).name)
        else:
            last_sale = area_order_info[order.area_id][0]
            area_order_info[order.area_id] = (last_sale + float(order.total), area_order_info[order.area_id][1])

    area_info = {}
    area_info['area_order_info'] = area_order_info

    divsion = len(last_validate_order_list)
    if divsion == 0:
        divsion = 1
    order_rate = ((len(validate_order_list) - len(last_validate_order_list)) / divsion) * 100

    return JsonResponse({'data': {'all_order_list': all_order_list, 'sale_total': sale_total,
                                  'validate_order_list':validate_order_list, 'tax_total': tax_total,
                                  'refund_order': refund_order, 'area_info': area_info, 'order_rate': order_rate}})

