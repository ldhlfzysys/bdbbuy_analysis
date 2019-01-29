
from django.urls import path


from .views import *

urlpatterns = [

    path('getAuth', getAdminUserAuth),

]