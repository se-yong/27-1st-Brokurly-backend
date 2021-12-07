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
            data = json.loads(request.body)
            cart = Cart.objects.filter(user=request.user, product = data['product_id'])
            
            if cart.exists():
                quantity = cart[0].quantity + data['quantity']
                cart.update(quantity = quantity)
                
                return JsonResponse({'message' : 'UPDATE'}, status = 200)
        
            Cart.objects.create(
                user     = User.objects.get(id=request.user),
                product  = Product.objects.get(id = data['product_id']),
                quantity = data['quantity']
            )

            return JsonResponse({'messages' : 'CREATED'}, status = 201)
        
        except KeyError:
            return JsonResponse({'messages' : 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'messages' : 'INVALID_USER'}, status = 404)
        
        except Product.DoesNotExist:
            return JsonResponse({'messages' : 'INVALID_PRODUCT'}, status = 404)

    @login_required
    def get(self, request):
        carts  = Cart.objects.filter(user = request.user)
        result = []
        if not carts.exists():
            return JsonResponse ({'result' : result}, status = 404 )
        
        result = [{
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
        
            cart = Cart.objects.filter(user = request.user, product = data['product_id'])
        
            if not cart.exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 404)

            cart.update(quantity = data['quantity'])
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' :'KEY_ERROR'}, status = 400)
    
    @login_required
    def delete(self, request):
        try:
            product = request.headers['product']
            cart    = Cart.objects.filter(user = 1, product = product)

            if cart.exists():
                cart.delete()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
            return JsonResponse({'message' : 'INVALID_CART'}, status = 404)
        
        except KeyError:
            return JsonResponse({'message : KEY_ERROR'}, status = 400)