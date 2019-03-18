
from django.urls import path


from .views import *

urlpatterns = [

    path('getOrderList', get_order_list),
    path('getDriverDeliveredOrder', get_driver_delivered_order)

]