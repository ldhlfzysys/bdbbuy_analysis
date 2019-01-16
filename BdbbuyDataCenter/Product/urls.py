
from django.urls import path


from .views import *

urlpatterns = [

    path('getWarnigProduct', get_out_of_date_product),
    path('getProductSale', get_product_sale),
    path('getProductCatogery', get_product_catogery)

]