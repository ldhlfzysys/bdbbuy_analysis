from django.db import models
from django.db.models import Q

from enum import Enum

# custom
from Tools.model_util import CModel
from datetime import datetime, timedelta
from django.utils import timezone
from Order.views import Orders
from Tools.time_util import *
import json

# Create your models here.

LOW_QTY_COUNT = 5

class ProductStatus(Enum):
    ProductAll=0
    ProductOnsale=1
    ProductOffsale=2



class Category(CModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class CategoryProduct(CModel):
    product_id = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_product'
        unique_together = (('product_id', 'category_id'),)


class Product(CModel):
    product_id = models.AutoField(primary_key=True)
    sku = models.CharField(unique=True, max_length=50, blank=True, null=True)
    en_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=11, blank=True, null=True)
    purchase_price = models.CharField(max_length=11, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    manufacturer = models.CharField(max_length=30, blank=True, null=True)
    images_num = models.IntegerField(blank=True, null=True)
    search_key = models.CharField(max_length=300, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    tax_id = models.CharField(max_length=11, blank=True, null=True)
    shop_ids = models.TextField(blank=True, null=True)
    cat_ids = models.CharField(max_length=200, blank=True, null=True)
    special_price = models.CharField(max_length=11, blank=True, null=True)
    special_price_start = models.CharField(max_length=32, blank=True, null=True)
    special_price_end = models.CharField(max_length=32, blank=True, null=True)
    total_sell = models.IntegerField()
    create_at = models.CharField(max_length=30, blank=True, null=True)
    quality_date = models.CharField(max_length=30, blank=True, null=True)
    show_index = models.IntegerField(blank=True, null=True)
    buy_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'

    @classmethod
    def get_product(cls, **kwargs):
        product = None
        try:
            product = Product.objects.get(**kwargs)
        except Exception as e:
            print(e)
        return product

    @classmethod
    def get_lowcount_outofdate_products(cls, **kwargs):
        low_count = kwargs.get('low_count', None)
        out_of_date = kwargs.get('out_of_date', False)
        order_day = kwargs.get('order_day', None)
        products = []
        if low_count:
            # 按库存数进行查找
            for stock in ProductStock.get_low_qty_data(low_count=low_count):
                product_list = Product.objects.filter(product_id=stock.product_id)
                if product_list and len(product_list) > 0:
                    product = product_list[0]
                    if ProductStatus.ProductOnsale.value == product.status:
                        products.append(product.toJson())

        if out_of_date:
            # 查找过期的在线商品
            product_list = Product.objects.exclude((Q(quality_date='') | Q(quality_date__isnull=True)))\
                                          .filter(Q(status=ProductStatus.ProductOnsale.value),
                                                  Q(quality_date__lt=datetime.now()))
            products.extend([product.toJson() for product in product_list])

        if order_day:
            # 按照过去一段时间销量查找库存较少数据
            product_list = Product.objects.filter(status=ProductStatus.ProductOnsale.value)
            date_now = datetime.now().replace(hour=0, minute=0, second=0)
            from_date = (date_now - timedelta(days=int(order_day))).replace(tzinfo=timezone.utc)
            to_date = datetime.now().replace(tzinfo=timezone.utc)
            order_list = Orders.objects.filter(create_at__range=(from_date, to_date)).values('product_desc')
            order_dict = {}
            for order in order_list.iterator():
                for order_product in json.loads(order['product_desc']):
                    product_id = str(order_product['product_id'])
                    product_count = int(order_product['product_count'])
                    if order_dict.get(product_id, None):
                        order_dict[product_id] = order_dict[product_id] + product_count
                    else:
                        order_dict[product_id] = product_count


            for product in product_list:
                stock_count = ProductStock.get_product_stock(product_id=product.product_id)
                product_id_str = str(product.product_id)
                if order_dict.get(product_id_str, None):
                    if stock_count <= order_dict[product_id_str]:
                        product_dic = product.toJson()
                        product_dic['order_count'] = order_dict[product_id_str]
                        product_dic['delta_count'] =  order_dict[product_id_str] - stock_count
                        products.append(product_dic)
                else:
                    if stock_count <= LOW_QTY_COUNT:
                        product_dic = product.toJson()
                        product_dic['order_count'] = 0
                        product_dic['delta_count'] = LOW_QTY_COUNT - stock_count
                        products.append(product_dic)
        return products

    def toJson(self):
        product_qty = ProductStock.get_product_stock(product_id=self.product_id)
        json_dic = {
            'product_id': self.product_id,
            'sku': self.sku,
            'en_name': self.en_name,
            'name': self.name,
            'price': self.price,
            'purchase_price': self.purchase_price,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'images_num': self.images_num,
            'search_key': self.search_key,
            'status': self.status,
            'tax_id': self.tax_id,
            'shop_ids': self.shop_ids,
            'cat_ids': self.cat_ids,
            'special_price': self.special_price,
            'special_price_start': self.special_price_start,
            'special_price_end': self.special_price_end,
            'total_sell': self.total_sell,
            'create_at': self.create_at,
            'quality_date': self.quality_date,
            'show_index': self.show_index,
            'product_qty': product_qty
        }
        return json_dic




class ProductComment(CModel):
    product_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_at = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_comment'


class ProductDetail(CModel):
    product_id = models.IntegerField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_detail'


class ProductOrder(CModel):
    product_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_order'


class ProductStock(CModel):
    shop_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_stock'
        unique_together = (('shop_id', 'product_id'),)

    @classmethod
    def get_low_qty_data(cls, low_count):
        product_list = ProductStock.objects.filter(qty__lte=low_count)
        return product_list

    @classmethod
    def if_low(cls, product_id, low_count):
        result = False
        try:
            product = ProductStock.objects.get(product_id=product_id)
            result = (product and int(product.qty) < low_count)
        except Exception as e:
            result = True

        return result

    @classmethod
    def get_product_stock(cls, product_id):
        count = None
        try:
            product = ProductStock.objects.get(product_id=product_id)
            count = product.qty
        except Exception as e:
            print(e)
        return count




class ProductTierPrice(CModel):
    product_id = models.IntegerField(blank=True, null=True)
    tier_price = models.CharField(max_length=30, blank=True, null=True)
    tier_count = models.IntegerField(blank=True, null=True)
    customer_group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_tier_price'
        unique_together = (('product_id', 'customer_group_id'),)