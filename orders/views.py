import json

from django.http            import JsonResponse
from django.views           import View
from django.db              import transaction, DataError
from django.db.models       import Q

from .models         import Order, OrderStatus, OrderItem, OrderItemsStatus
from cart.models     import Cart
from core.decorator  import login_required

class OrderView(View):
    @login_required
    def post(self, request):
        try:
            STATUS               = 1
            data                 = json.loads(request.body)
            order_status         = OrderStatus.objects.get(id=STATUS)
            order_items_status   = OrderItemsStatus.objects.get(id=STATUS)
            cartItem             = Q()

            for item in data:
                cartItem |= Q(id=item['cart_id'])
            
            carts = Cart.objects.filter(cartItem)
            if carts.exists():
                return JsonResponse({"message":"INVALID_CART"},status=201)

            with transaction.atomic():
                order = Order.objects.create(order_status=order_status, users=request.user)
                bulk_list = [OrderItem(
                    product            = cart.product,
                    quantity           = cart.quantity,
                    order              = order,
                    order_items_status = order_items_status,
                    )for cart in carts]
                carts.delete()
                OrderItem.objects.bulk_create(bulk_list)
                
            return JsonResponse({"message":"CREATE"},status=201)
                
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_STATUS"},status=404)
        except OrderItemsStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_ITEMS_STATUS"},status=404)
        except DataError:
            return JsonResponse({"message":"DATA_ERROR"},status = 400)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=400)
    
    @login_required
    def get(self, request):
            orders = Order.objects.filter(users=request.user).prefetch_related(
                "orderitem_set",
                "orderitem_set__product__image_set",
                "orderitem_set__order_items_status").select_related("order_status")
                
            result=[]
            if not orders.exists():
                return JsonResponse({"result":result},status=404)

            result=[
                {
                "order_id"     : order.id,
                "order_number" : order.order_number,
                "order_status" : order.order_status.status,
                "products"     : [{
                "id"           : orderItem.product.id,
                "name"         : orderItem.product.name,
                "image"        : orderItem.product.image_set.all()[0].url,
                "price"        : orderItem.product.price,
                "quantity"     : orderItem.quantity,
                "status"       : orderItem.order_items_status.status,
                }for orderItem in order.orderitem_set.all()]
                }for order in orders]

            return JsonResponse({"result":result},status=200)

    @login_required
    def patch(self, request):
        try:
            STATUS      = 10
            data        = json.loads(request.body)
            orderStatus = OrderStatus.objects.get(id=STATUS)
            itemsStatus = OrderItemsStatus.objects.get(id=STATUS)
            
            with transaction.atomic():
                if Order.objects.filter(id=data["order_id"]).exists():
                    order = Order.objects.filter(id=data["order_id"])
                    order.update(order_status=orderStatus)
                    order[0].orderitem_set.all().update(order_items_status=itemsStatus)
            
                    return JsonResponse({"message":"SUCCESS"},status=200)

                return JsonResponse({"message":"INVALID_ORDER_ID"},status=400)

        except KeyError: 
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except OrderStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_STATUS"},status=404)
        except OrderItemsStatus.DoesNotExist:
            return JsonResponse({"message":"INVALID_ORDER_ITEMS_STATUS"},status=404)
        except transaction.TransactionManagementError:
            return JsonResponse({"message":"TRANSACTION_ERROR"},status=400)