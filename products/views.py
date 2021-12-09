from django.core.exceptions import MultipleObjectsReturned
from django.http  import JsonResponse
from django.views import View

from .models import Product
from products.models import Product, Category, Menu

class ProductView(View):
    def get(self, request):

        try:
            menu_name     = request.GET.get('menu', None)
            category_name = request.GET.get('category', None) 
            sort          = request.GET.get('sort', '-created_at')
            
            sort_dict = {
                '-created_at' : '-created_at',
                'price'       : 'price',
                '-price'      : '-price'
            }

            if menu_name:
                menu     = Menu.objects.get(name=menu_name)
                products = Product.objects.filter(category__menu=menu).order_by(sort_dict[sort])

            if category_name:
                category = Category.objects.get(name=category_name)
                products = category.product_set.all().order_by(sort_dict[sort])

            results = [
                {
                    'id'           : product_data.id,
                    'name'         : product_data.name,
                    'introduction' : product_data.introduction,
                    'price'        : product_data.price,
                    'image'        : [image.url for image in product_data.image_set.all()]
                }for product_data in products]
             
            return JsonResponse({'result':results}, status=200)

        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'CategoryDoesNotExist'}, status=400)

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
            "itemPackage"  : product.package,
            "origin"       : product.origin,
            "weight"       : product.weight,
            "images"       : product.image_set.all()[0].url
            }

            return JsonResponse({"result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "INVALID_PRODUCT"}, status = 404)