from django.http     import JsonResponse
from django.views    import View

from products.models import Product, Category, Menu

class ProductView(View):
    def get(self, request):
        try:
            category_id = request.GET.get('category', 'all')
            sort        = request.GET.get('sort', 0)
            sort_dict   = {
                0 : 'created_at',
                1 : 'price',
                2 : '-price',
                3 : 'name'
            }

            if category_id == 'all':
                products = Product.objects.all()
                results = []
                for data_all in products:
                    results.append(
                            {
                                'name'         : data_all.name,
                                'introduction' : data_all.introduction,
                                'price'        : data_all.price,
                                'image'        : [image.url for image in data_all.image_set.all()]
                            }
                        )
                print(results)
                return JsonResponse({'result':results}, status=201)



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

            print(results)
            return JsonResponse({'result':results}, status=201)

        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DoesNotExits'}, status=500)