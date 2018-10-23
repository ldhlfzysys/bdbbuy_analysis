"""BdbbuyDataCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings

from Order import urls as order_urls
from Product import urls as product_urls

urlpatterns_debug = [
    path('admin/', admin.site.urls),
    path('order/', include(order_urls)),
    path('product/', include(product_urls))
]

urlpatterns_production = [
    path('bdbbuyanalysisserver/admin/', admin.site.urls),
    path('bdbbuyanalysisserver/order/', include(order_urls)),
    path('bdbbuyanalysisserver/product/', include(product_urls))
]

urlpatterns = urlpatterns_debug
if (not settings.DEBUG):
    urlpatterns = urlpatterns_production
