from django.http     import JsonResponse
from django.views    import View

from products.models import Product, Category

class ProductView(View):
    def get(self, request):
        try:
            category_id = request.GET.get('category', '채소')
            sort = request.GET.get('sort', '0')
            sort_dict = {
                '0' : 'created_at',
                '1' : 'price',
                '2' : '-price'
            }
            category = Category.objects.get(name=category_id)
            products = Product.objects.filter(category=category).all().order_by(sort_dict[sort])
            results  = []
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
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DoesNotExits'}, status=500)