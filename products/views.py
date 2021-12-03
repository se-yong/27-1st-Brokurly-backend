from django.http  import JsonResponse
from django.views import View

from .models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            
            result = {
              "id"           : product.id,
              "name"         : product.name,
              "price"        : product.price,
              "introduction" : product.introduction,
              "description"  : product.description,
              "unit"         : product.unit,
              "shipping"     : product.shipping,
              "package"      : product.package,
              "origin"       : product.origin,
              "weight"       : product.weight,
              "images"       : [image.url for image in product.image_set.all()]
            }

            return JsonResponse({"result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "INVALID_PRODUCT"}, status = 401)
        
