import json

from django.http            import JsonResponse
from django.views           import View
from django.db              import transaction, DataError

from .models     import Order, OrderStatus, OrderItem, OrderItemsStatus
from cart.models import Cart

class OrderView(View):
    # @데코레이터(token) 들어갈 자리
    def post(self, request):
        try:
            data                 = json.loads(request.body)
            order_status         = OrderStatus.objects.get(id=1)
            order_items_status   = OrderItemsStatus.objects.get(id=1)

            with transaction.atomic():
                order = Order.objects.create(order_status=order_status, users=request.user)
                bulk_order_item_list = []
            
                for item in data:
                    bulk_order_item_list.append(
                        OrderItem(
                            product            = item["product_id"],
                            quantity           = item["quantity"],
                            order              = order,
                            order_items_status = order_items_status,
                            ))
                    Cart.objects.get(product=item["product_id"]).delete()
                OrderItem.objects.bulk_create(bulk_order_item_list)
                
            return JsonResponse({"message":"SUCCESS"},status=201)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_STATUS"},status=401)
        except OrderItemsStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_ITEMS_STATUS"},status=401)
        except Cart.DoesNotExist:
            return JsonResponse({"message":"INVALID_CART"},status=401)
        except DataError:
            return JsonResponse({"message":"DATA_ERROR"},status = 401)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=401)
    
    # @데코레이터(token) 들어갈 자리
    def get(self, request):
        try:
            orders = Order.objects.filter(users=request.user).prefetch_related(
                "orderitem_set",
                "orderitem_set__product__image_set",
                "orderitem_set__order_items_status").select_related("order_status")
            
            result=[]
            if not orders.exists():
                return JsonResponse({"message":result},status=201)
                
            for order in orders:
                resultItem={
                    "order_id"     : order.id,
                    "order_number" : order.order_number,
                    "order_status" : order.order_status.status,
                    }

                resultItem_list=[]
                for orderItem in order.orderitem_set.all():
                    resultItem_list.append({
                        "id"       : orderItem.product.id,
                        "name"     : orderItem.product.name,
                        "image"    : orderItem.product.image_set.all()[0].url,
                        "price"    : orderItem.product.price,
                        "quentity" : orderItem.quantity,
                        "status"   : orderItem.order_items_status.status,

                    })
                resultItem["products"] = resultItem_list
                result.append(resultItem)

            return JsonResponse({"message":result},status=201)
            
        except Exception:
            return JsonResponse({"message":"ERROR"},status=401)

    # @데코레이터 들어갈자리
    def patch(self, request):
        try:
            data        = json.loads(request.body)
            orderStatus = OrderStatus.objects.get(id=9)
            itemsStatus = OrderItemsStatus.objects.get(id=9)

            with transaction.atomic():
                if Order.objects.filter(id=data["order_id"]).exists():
                    order = Order.objects.filter(id=data["order_id"]).update(order_status=orderStatus)
                    order.orderitem_set.all().update(order_items_status=itemsStatus)
            
                    return JsonResponse({"message":"SUCCESS"},status=201)

                return JsonResponse({"message":"INVALID_ORDER_ID"},status=401)

        except KeyError: 
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_STATUS"},status=401)
        except OrderItemsStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_ITEMS_STATUS"},status=401)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=401)