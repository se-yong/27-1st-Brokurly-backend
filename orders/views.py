from django.http  import JsonResponse
from django.views import View

from .models      import Order, OrderStatus, OrderItem, OrderItemsStatus
from users.models import User
from cart.models  import Cart

class OrderView(View):
    # @데코레이터(token) 들어갈 자리
    def post(self, request):
        
        return JsonResponse({},status=200)
# Create your views here.
