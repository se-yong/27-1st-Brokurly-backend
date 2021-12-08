import json, uuid
from enum import Enum

from django.http            import JsonResponse
from django.views           import View
from django.db              import transaction, DataError

from .models         import Order, OrderItem
from cart.models     import Cart
from core.decorator  import login_required

class OrderStatus(Enum):    
    WAIT_DEPOSIT       = 1   
    COMPLETION_DEPOSIT = 2    
    READY_RELEASE      = 3  
    SHIPMENT_COMPLETE  = 4
    DELIVERED          = 5
    DELAYED_DELIVERY   = 6
    DELIVERY_COMPLETED = 7
    ORDER_COMPLETE     = 8
    ORDER_CANCELLATION = 9    

class OrderView(View):
    @login_required
    def post(self, request):
        try:
            data     = json.loads(request.body)
            cart_ids = data["cart_ids"]     
            carts    = Cart.objects.filter(id__in=cart_ids,user=request.user)

            if not carts.exists():
                return JsonResponse({"message":"INVALID_CART"},status=404)
            
            with transaction.atomic():
                order = Order.objects.create(
                    order_status_id = OrderStatus.WAIT_DEPOSIT.value, 
                    users           = request.user,
                    order_number    = uuid.uuid4()
                    )
                bulk_list = [OrderItem(
                    product               = cart.product,
                    quantity              = cart.quantity,
                    order                 = order,
                    order_items_status_id = OrderStatus.WAIT_DEPOSIT.value,
                    ) for cart in carts]
                carts.delete()
                OrderItem.objects.bulk_create(bulk_list)
                
            return JsonResponse({"message":"CREATE"},status=201)
                
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except DataError:
            return JsonResponse({"message":"DATA_ERROR"},status = 400)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=400)
    
    @login_required
    def get(self, request):
            orders = Order.objects.filter(users=request.user).select_related("order_status")\
                                                             .prefetch_related("orderitem_set__product__image_set",
                                                                               "orderitem_set__order_items_status").order_by("-created_at")
           
            result=[{
                "order_id"     : order.id,
                "order_number" : order.order_number,
                "order_status" : order.order_status.status,
                "products"     : [{
                    "id"       : orderItem.product.id,
                    "name"     : orderItem.product.name,
                    "image"    : orderItem.product.image_set.all()[0].url,
                    "price"    : orderItem.product.price,
                    "quantity" : orderItem.quantity,
                    "status"   : orderItem.order_items_status.status,
                } for orderItem in order.orderitem_set.all()]
            } for order in orders]

            return JsonResponse({"result":result},status=200)

    @login_required
    def patch(self, request):
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                order = Order.objects.get(id=data["order_id"])
                order.order_status_id = OrderStatus.ORDER_CANCELLATION.value
                order.save()
                order.orderitem_set.all().update(order_items_status=OrderStatus.ORDER_CANCELLATION.value)
        
                return JsonResponse({"message":"SUCCESS"},status=200)

        except KeyError: 
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except Order.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER"},status=404)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=400)