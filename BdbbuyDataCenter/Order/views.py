from django.shortcuts import render

import json

from datetime import datetime,timedelta
# django

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# custom
from .models import *



# Create your views here.

@require_http_methods(["GET"])
def get_order_list(request):
    default_from_date = datetime.now().replace(hour=0, minute=0, second=0)
    search_from_date = request.GET.get('fromDate', default_from_date)
    search_to_date = request.GET.get('toDate', datetime.now())
    areas = request.GET.get('areaId', 'all')
    order_list_q = Orders.objects.filter(create_at__gte=search_from_date, create_at__lte=search_to_date)
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

    return JsonResponse({'data': {'all_order_list': all_order_list, 'sale_total': sale_total,
                                  'validate_order_list':validate_order_list, 'tax_total': tax_total,
                                  'refund_order': refund_order}})

