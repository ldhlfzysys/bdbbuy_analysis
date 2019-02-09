from django.shortcuts import render


from .models import *

# django
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from  Order.models import Orders, OrderStatus

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

@require_http_methods(["GET"])
def get_product_sale(request):
    product_list = []
    default_from_date = datetime.now().replace(hour=0, minute=0, second=0)
    search_from_date = request.GET.get('fromDate', default_from_date)
    search_to_date = request.GET.get('toDate', datetime.now())
    catogery = request.GET.get('catogeryId', 'all')

    all_order_q = Orders.objects.filter(Q(create_at__range=(search_from_date, search_to_date)),
                                        ~Q(status__in=[OrderStatus.OrderNotPay.value, OrderStatus.OrderDelete.value,
                                                       OrderStatus.OrderTimeout.value])).values('product_desc')
    product_dic = {}

    for order in all_order_q.iterator():
        for order_product in json.loads(order['product_desc']):
            product_id = str(order_product['product_id'])
            product_count = int(order_product['product_count'])
            if product_dic.get(product_id, None):
                product_dic[product_id] += product_count
            else:
                product_dic[product_id] = product_count

    all_product_q = Product.objects.filter(product_id__in=product_dic.keys())

    if catogery == 'all':
        for product in all_product_q:
            dic = product.toJson()
            dic['sale_count'] = product_dic[str(product.product_id)]
            product_list.append(dic)
    else:
        print('分类筛选')
        catogery_product_q = CategoryProduct.objects.filter(product_id__in=product_dic.keys())
        all_catogery_ids = Category.objects.filter(Q(category_id=catogery) | Q(parent_id=catogery)).distinct()

        cat_dic = {}
        for catogery in all_catogery_ids:
            catogery_id = str(catogery.category_id)
            cat_dic[catogery_id] = catogery_id

        catogery_product_dic = {}
        for catogery_product in catogery_product_q:
            if cat_dic.get(str(catogery_product.category_id), None):
                catogery_product_id = str(catogery_product.product_id)
                catogery_product_dic[catogery_product_id] = catogery_product_id

        for product in all_product_q:
            if catogery_product_dic.get(str(product.product_id), None):
                dic = product.toJson()
                dic['sale_count'] = product_dic[str(product.product_id)]
                product_list.append(dic)

    product_list = sorted(product_list, key=lambda product: product['sale_count'], reverse=True)
    return JsonResponse({'data': {'product_list': product_list, 'totalCount': len(product_list)}})


@require_http_methods(["GET"])
def get_sale_group_by_catogery_id(request):

    statistic_list = []
    default_from_date = datetime.now().replace(hour=0, minute=0, second=0)
    search_from_date = request.GET.get('fromDate', default_from_date)
    search_to_date = request.GET.get('toDate', datetime.now())

    all_order_q = Orders.objects.filter(Q(create_at__range=(search_from_date, search_to_date)),
                                        ~Q(status__in=[OrderStatus.OrderNotPay.value, OrderStatus.OrderDelete.value,
                                                       OrderStatus.OrderTimeout.value])).values('product_desc')
    product_dic = {}

    for order in all_order_q.iterator():
        for order_product in json.loads(order['product_desc']):
            product_id = str(order_product['product_id'])
            product_count = int(order_product['product_count'])
            if product_dic.get(product_id, None):
                product_dic[product_id] += product_count
            else:
                product_dic[product_id] = product_count

    catogery_product_q = CategoryProduct.objects.filter(product_id__in=product_dic.keys())

    sub_catogery_dic = {}

    # 计算所有小分类的销量
    for catogery_product in catogery_product_q:
        catogery_id = str(catogery_product.category_id)
        product_id = str(catogery_product.product_id)
        if sub_catogery_dic.get(catogery_id, None):
            sub_catogery_dic[catogery_id] += product_dic[product_id]
        else:
            sub_catogery_dic[catogery_id] = product_dic[product_id]

    statistic_dic = {}

    for (sub_catogery_id, sale) in sub_catogery_dic.items():
        parent_catogery =  get_sub_catogery(sub_catogery_id, 5)
        if parent_catogery != '':
            parent_catogery_id = str(parent_catogery.category_id)
            if statistic_dic.get(parent_catogery_id, None):
                statistic_dic[parent_catogery_id]['catogery_sale'] += sub_catogery_dic[sub_catogery_id]
            else:
                statistic_dic[parent_catogery_id] = {}
                statistic_dic[parent_catogery_id]['catogery_sale'] = sub_catogery_dic[sub_catogery_id]
                statistic_dic[parent_catogery_id]['catogery_name'] = parent_catogery.name

    for (cat_id, dic) in statistic_dic.items():
        cat_dic = {'catogery_id': cat_id,
                   'catogery_name': dic['catogery_name'],
                   'catogery_sale': dic['catogery_sale']}

        statistic_list.append(cat_dic)

    return JsonResponse({'data': {'statistic_list': statistic_list}})


def get_sub_catogery(catogery_id, max_search_times):
    if max_search_times <= 0:
        return ''
    try:
        catogery = Category.objects.get(category_id=catogery_id)
        if catogery.parent_id == 2:
            return catogery
        else:
            return get_sub_catogery(catogery.parent_id, max_search_times-1)
    except Exception as e:
        return ''

@require_http_methods(["GET"])
def get_product_catogery(request):
    catogery_list = []

    all_catogery_q = Category.objects.filter(parent_id=2)

    for catogery in all_catogery_q.iterator():
        sub_catogery_list = []
        for sub_catogery in Category.objects.filter(parent_id=catogery.category_id):
            sub_catogery_dic = {"catogery_id": sub_catogery.category_id, "catogery_name": sub_catogery.name}
            sub_catogery_list.append(sub_catogery_dic)
        catogery_dic = {"catogery_id": catogery.category_id, "catogery_name": catogery.name, "catogery_sublist": sub_catogery_list}
        catogery_list.append(catogery_dic)

    return JsonResponse({'data': {'catogery_list': catogery_list}})
