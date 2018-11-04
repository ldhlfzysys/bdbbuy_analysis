
from django.urls import path


from .views import *

urlpatterns = [

    path('getOrderList', get_order_list),

]