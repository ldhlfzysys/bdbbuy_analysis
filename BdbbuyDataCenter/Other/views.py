from django.shortcuts import render

# Create your views here.


from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_area_list(request):
    area_list = [i.serializable_values() for i in Area.objects.all()]
    return JsonResponse({'data': {'area_list': area_list}})
