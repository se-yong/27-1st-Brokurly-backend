from django.http import JsonResponse
from django.views import View

from .models import Product

class ProductDetailView(View):
  def get(self,request):
    try:
      print(request.GET.get("id"))
      product=Product.objects.prefetch_related("image_set").get(id=request.GET.get("id"))
      
      result = {
        "product_name"         : product.name,
        "product_price"        : product.price,
        "product_introduction" : product.introduction,
        "product_description"  : product.description,
        "product_unit"         : product.unit,
        "product_shipping"     : product.shipping,
        "product_package"      : product.package,
        "product_origin"       : product.origin,
        "product_weight"       : product.weight,
        "image_url"            : [image.url for image in product.image_set.all()]
      } 
      return JsonResponse({"result":result},status=200)

    except Product.DoesNotExist : return JsonResponse({"message" : "INVALID_PRODUCT"},status = 401)
    except KeyError             : return JsonResponse({"message" : "KEY_ERROR"},status = 400)