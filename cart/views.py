import json

from django.http  import JsonResponse
from django.views import View

# from core.utils   import log_in_decorator
from users.models import User
from .models      import Cart
from products.models    import Product

class CartView(View):
    # @log_in_decorator
    def post(request, self):
        data = json.loads(request.body)
        cart = Cart.objects.filter(user=request.user, product = data['product_id'])
        
        if cart.exists():
            cart.quantity += data['quantity']
            cart.save()
            return JsonResponse({'message' : 'UPDATE'}, status = 200)
        
        Cart.objects.create(
            user = User.objects.get(id=request.user)
            product = Product.objects.get(id = data['product_id'])
            quantity = data['quantity']
        )

        return JsonResponse({'messages' : 'CREATED'}, status = 201)

