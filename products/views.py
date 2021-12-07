from django.core.exceptions import MultipleObjectsReturned
from django.http  import JsonResponse
from django.views import View

from .models import Product
from products.models import Product, Category, Menu

class ProductView(View):
    def get(self, request):

        try:
            menu_name = request.GET.get('menu', None)
            sort      = request.GET.get('sort', 'created_at')
            sort_dict = {
                'created_at' : 'created_at',
                'price'      : 'price',
                '-price'     : '-price'
            }

            if menu_name   == '채소전체':
                menu_name  = '채소'
                menus      = Menu.objects.get(name=menu_name)
                categories = Category.objects.filter(menu=menus).all()
                products   = Product.objects.filter(category__in=categories).all().order_by(sort_dict[sort])
                results    = []

            elif menu_name == '샐러드전체':
                menu_name  = '샐러드'
                menus      = Menu.objects.get(name=menu_name)
                categories = Category.objects.filter(menu=menus).all()
                products   = Product.objects.filter(category__in=categories).all().order_by(sort_dict[sort])
                results    = []

            elif menu_name == '과일전체':
                menu_name  = '과일'
                menus      = Menu.objects.get(name=menu_name)
                categories = Category.objects.filter(menu=menus).all()
                products   = Product.objects.filter(category__in=categories).all().order_by(sort_dict[sort])
                results    = []

            elif menu_name == '간편식전체':
                menu_name  = '간편식'
                menus      = Menu.objects.get(name=menu_name)
                categories = Category.objects.filter(menu=menus).all()
                products   = Product.objects.filter(category__in=categories).all().order_by(sort_dict[sort])
                results    = []

            if menu_name:
                menus      = Menu.objects.get(name=menu_name)
                categories = Category.objects.filter(menu=menus).all()
                products   = Product.objects.filter(category__in=categories).all().order_by(sort_dict[sort])
                # products = Product.objects.filter(category__menu_id=menu_name).all()
                results    = []

            for product_data in products:
                results.append(
                    {
                        'name'         : product_data.name,
                        'introduction' : product_data.introduction,
                        'price'        : product_data.price,
                        'image'        : [image.url for image in product_data.image_set.all()]
                    }
                )
            
            return JsonResponse({'result':results}, status=201)

        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DoesNotExits'}, status=500)

class CategoryView(View):
    def get(self, request):
        try:
            category_name = request.GET.get('category', None) 
            sort          = request.GET.get('sort', 'created_at')
            sort_dict     = {
                'created_at' : 'created_at',
                'price'      : 'price',
                '-price'     : '-price'
            }
                
            if category_name:
                categories = Category.objects.get(name=category_name)
                products   = Product.objects.filter(category=categories).all().order_by(sort_dict[sort])
                # products = Product.objects.filter(category_id=category_id, category__menu_id=menu_id).all().order_by(sort_dict[sort])
                results    = []

            for product_data in products:
                results.append(
                    {
                        'name'         : product_data.name,
                        'introduction' : product_data.introduction,
                        'price'        : product_data.price,
                        'image'        : [image.url for image in product_data.image_set.all()]
                    }
                )
            
            return JsonResponse({'result':results}, status=201)

        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DoesNotExits'}, status=500)

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