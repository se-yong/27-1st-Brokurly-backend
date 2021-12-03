from django.urls import path

from .views import ProductDetailView

urlpatterns = [
  path("/product",ProductDetailView.as_view(),)
]
