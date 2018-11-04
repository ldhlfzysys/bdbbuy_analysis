
from django.urls import path


from .views import *


urlpatterns = [

    path('getAreaList', get_area_list),

]