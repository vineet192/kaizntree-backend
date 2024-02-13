from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kaizntree.serializers import InventoryItemSerializer
from kaizntree.models import InventoryItem
from kaizntree.exceptions import MalformedNumericalFilter
from firebase_admin import auth
from django.db.models import Q
from datetime import datetime

class Inventory(APIView):

    @csrf_exempt
    def get(self, request):

        uid = None

        #Securely resolve the uid from the firebase token
        try:
            firebase_auth_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            decoded_token = auth.verify_id_token(firebase_auth_token, clock_skew_seconds=10)
            uid = decoded_token['uid']
        except Exception as e:
            return JsonResponse(status=401, data={"msg": "User could not be resolved"})

        try:
            filters = self.build_filter_kwargs(request.query_params, uid)
        except MalformedNumericalFilter:
            return JsonResponse(status=400, data={"msg": "A numerical filter was malformed"})

        inventory_items = InventoryItem.objects.filter(filters).all()

        inventory_items_serialized = InventoryItemSerializer(inventory_items, many=True)

        return JsonResponse(status=200, data=inventory_items_serialized.data, safe=False)

    @csrf_exempt
    def post(self, request):

        uid = None

        #Securely resolve the uid from the firebase token
        try:
            firebase_auth_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            decoded_token = auth.verify_id_token(firebase_auth_token, clock_skew_seconds=10)
            uid = decoded_token['uid']
        except Exception as e:
            print(e)
            return JsonResponse(status=401, data={"msg": "User could not be resolved"})
        
        inventory_data = dict(request.data)
        inventory_data["user_id"] = uid

        inventory_item = InventoryItemSerializer(data=inventory_data)

        if not inventory_item.is_valid():
            return JsonResponse(status=400, data=inventory_item.errors)
        
        try:
            inventory_item.save()
        except Exception as e:
            return HttpResponse(status=400)
        return HttpResponse(status=201)
    
    """
    Helper function that builds Q query object from request query params

    Paramters
        query_params: dict
        uid: str

    Returns
        Q object to be used for filtering
    """
    def build_filter_kwargs(self, query_params, uid: str) -> Q:

        filters = Q()
        filters &= Q(user_id=uid)

        text_queries = Q()
        
        if "sku" in query_params:
            text_queries |= Q(sku__icontains=query_params["sku"].lower())

        if "name" in query_params:
            text_queries |= Q(name__icontains=query_params["name"].lower())
        
        if "category" in query_params:
            text_queries |= Q(category__icontains=query_params["category"].lower())

        filters &= text_queries

        if "min_in_stock" in query_params:
            try:
                filters &= Q(in_stock__gte=float(query_params["min_in_stock"]))
            except:
                raise MalformedNumericalFilter()

        if "max_in_stock" in query_params:
            try:
                filters &= Q(in_stock__lte=float(query_params["max_in_stock"]))
            except:
                raise MalformedNumericalFilter()

        if "min_avail_stock" in query_params:
            try:
                filters &= Q(available_stock__gte=float(query_params["min_avail_stock"]))
            except:
                raise MalformedNumericalFilter()

        if "max_avail_stock" in query_params:
            try:
                filters &= Q(available_stock__lte=float(query_params["max_avail_stock"]))
            except:
                raise MalformedNumericalFilter()

        if "created_after" in query_params:
            filters &= Q(created__gte=datetime.strptime(query_params["created_after"], "%Y-%m-%d"))

        if "created_before" in query_params:
            filters &= Q(created__lte=datetime.strptime(query_params["created_before"], "%Y-%m-%d"))

        if "tags" in query_params:

            tags = query_params["tags"].split(",")

            for tag in tags:
                filters &= Q(tags__icontains=tag.lower())

        return filters

