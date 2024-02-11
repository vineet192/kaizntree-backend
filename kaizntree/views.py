from typing import Any
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from kaizntree.serializers import InventoryItemSerializer

class Inventory(APIView):

    @csrf_exempt
    def get(self, request):
        return HttpResponse("Hello get world!")

    @csrf_exempt
    def post(self, request):

        inventory_item = InventoryItemSerializer(data=request.data)

        if not inventory_item.is_valid():
            return JsonResponse(status=400, data=inventory_item.errors)
        
        try:
            inventory_item.save()
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
        return HttpResponse("Hello post world!")
