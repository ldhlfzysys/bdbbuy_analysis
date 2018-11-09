from django.shortcuts import render


import json
from functools import reduce
from datetime import datetime,timedelta
from django.utils import timezone
from Tools.time_util import *
# django

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.db.models import Q

# custom
from .models import *
from Other.models import Area, Refunds



# Create your views here.

@require_http_methods(["GET"])
def get_order_list(request):
    default_from_date = datetime.now().replace(hour=0, minute=0, second=0)
    search_from_date = request.GET.get('fromDate', default_from_date)
    search_to_date = request.GET.get('toDate', datetime.now())
    timestamp1 = string2timestamp(search_from_date)
    timestamp2 = string2timestamp(search_to_date)

    last_timestamp = timestamp1 - (timestamp2 - timestamp1)
    dt = timestamp_datetime(last_timestamp).replace(tzinfo=timezone.utc)

    search_to_datetime = timestamp_datetime(timestamp2).replace(tzinfo=timezone.utc)
    search_from_datetime = timestamp_datetime(timestamp1).replace(tzinfo=timezone.utc)

    areas = request.GET.get('areaId', '')
    if areas == '':
        areas = 'all'

    all_order_q = Orders.objects.filter(Q(create_at__range=(dt, search_to_datetime)),
                                        ~Q(status__in=[OrderStatus.OrderNotPay.value, OrderStatus.OrderDelete.value,
                                                       OrderStatus.OrderTimeout.value, OrderStatus.OrderRefunded.value]))\
        .values('order_id', 'area_id', 'create_at', 'status', 'tax_total', 'total')\
        .order_by('create_at')

    area_order_info = {}
    last_validate_order_count = 0
    all_order_list = []
    validate_order_list = []
    sale_total = 0
    tax_total = 0
    refund_order = 0
    all_area_order_list = []

    all_order_id = [order['order_id'] for order in all_order_q.iterator()
                    if datetime_timestamp(order['create_at'], 's') >= timestamp1
                    and (areas.find('all') != -1 or str(order['area_id']) in areas.split('-'))]

    print(all_order_id)
    refund_list = Refunds.objects.filter(order_id__in=all_order_id, create_at__range=(search_from_datetime, search_to_datetime, )).values('refund', 'order_id', 'create_at')\
        .order_by('create_at')

    for refund in refund_list:
        print(refund['order_id'])
        print(refund['refund'])
        print(refund['create_at'])

    all_refund_list = [refund['refund'] / 100.0 for refund in refund_list.iterator()]
    print('ghhjjjjj')
    print(all_refund_list)
    refund_order = len(all_refund_list)
    refund_total = sum(all_refund_list)
    print(refund_total)

    for order in all_order_q.iterator():
        # 统计地区销售数据
        if area_order_info.get(order['area_id'], None) == None:
            try:
                area = Area.objects.get(id=order['area_id'])
                area_order_info[order['area_id']] = (float(order['total']), area.name)
            except Exception as e:
                print(e)
        else:
            last_sale = area_order_info[order['area_id']][0]
            area_order_info[order['area_id']] = (last_sale + float(order['total']), area_order_info[order['area_id']][1])

        if datetime_timestamp(order['create_at'], 's') >= timestamp1:
            # 当前需要统计的订单
            all_area_order_list.append(order)
            if areas.find('all') != -1 or str(order['area_id']) in areas.split('-'):
                all_order_list.append(order)
                sale_total += float(order['total'])
                tax_total += float(order['tax_total'])
                validate_order_list.append(order)
        else:
            # 前一个时期的订单
            if areas.find('all') != -1 or order['area_id'] in areas.split('-'):
                last_validate_order_count += 1

    area_info = {}
    area_info['area_order_info'] = area_order_info

    diversion = last_validate_order_count
    if diversion == 0:
        diversion = 1
    rate = [100, 1][diversion == 1]
    order_rate = ((len(validate_order_list) - last_validate_order_count) / diversion) * rate
    print(sale_total)
    order_total = sale_total
    sale_total -= refund_total
    sale_total -= tax_total

    return JsonResponse(dict(data={'all_order_list': all_order_list, 'sale_total': sale_total,
                                   'validate_order_list': validate_order_list, 'tax_total': tax_total,
                                   'refund_order': refund_order, 'area_info': area_info, 'order_rate': order_rate,
                                   'order_total': order_total, 'refund_total': refund_total},
                             ))




