from django.urls    import path
from products.views import ProductView

urlpatterns = [
    path('', ProductView.as_view())
]