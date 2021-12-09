import json

from django.http        import JsonResponse
from django.views       import View

from core.decorator     import login_required
from users.models       import User
from .models            import Cart
from products.models    import Product

class CartView(View):
    @login_required
    def post(self, request):
        try:    
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']
            
            cart, created  = Cart.objects.get_or_create(
                user_id    = request.user.id,
                product_id = product_id,
            )
            
            if not created:
                cart.quantity += quantity
                cart.save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            
            cart.quantity = quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 404)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT'}, status = 404)

    @login_required
    def get(self, request):
        
        carts  = Cart.objects.select_related('product').filter(user = request.user)
        result = [{
            'cart_id'         : item.id,
            'quantity'        : item.quantity,
            'product_id'      : item.product.id,
            'product_price'   : item.product.price,
            'product_package' : item.product.package,
            'product_name'    : item.product.name,
            'product_image'   : item.product.image_set.all()[0].url
            } for item in carts.select_related('product').all()]
        return JsonResponse({'result' : result}, status = 200)      

    @login_required
    def patch(self, request):
        try:
            data = json.loads(request.body)
        
            cart = Cart.objects.get(id = data['cart_id'])

            cart.quantity = data['quantity']
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' :'KEY_ERROR'}, status = 400)
    
    @login_required
    def delete(self, request):
        try:
            data = json.loads(request.body)
            Cart.objects.filter(id__in=data['cart_id']).delete()
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status = 404)
        
        except KeyError:
            return JsonResponse({'message : KEY_ERROR'}, status = 400)