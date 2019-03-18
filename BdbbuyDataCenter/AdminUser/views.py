from django.shortcuts import render

# Create your views here.

import json
import urllib
import urllib.request
from urllib.parse import quote

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.db.models import Q


from .models import *


# Base_host = "http://localhost:1118/"
Base_host = "https://m.bdbbuy.com/"

@require_http_methods(["GET"])
def getAdminUserAuth(request):
    user = request.GET.get('user', '')
    auth_n = -1
    if user != '':
        print(user)
        url = Base_host + "api/index/adminusername?cookie_info=" + quote(user, 'utf-8')
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request, timeout=60)
            content = response.read().decode('utf8')
            result = json.loads(content)
            response.close()
        except Exception as e:
            print(e)
        admin_user_name = result['user_name']
        admin_user = Adminuser.objects.get(name=admin_user_name)
        for auth in admin_user.auth.split(','):
            auth_num = int(auth)
            if auth_num == 23 or auth_num == 25:
                auth_n = auth_num
                break
    return JsonResponse({'data': {'auth': auth_n, 'user_name': admin_user_name}})

@require_http_methods(["GET"])
def getDriverInfo(request):
    driver_list = [driver.toInfoJson() for driver in Adminuser.getDriverList()]
    return JsonResponse({"data": driver_list})
