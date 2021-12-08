from django.db   import models

from core.models import TimeStampModel

class Menu(TimeStampModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'menus'

    def __str__(self):
        return self.name

class Category(TimeStampModel):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Product(TimeStampModel):
    name               = models.CharField(max_length=100)
    introduction       = models.CharField(max_length=200)
    description        = models.TextField()
    unit               = models.CharField(max_length=10)
    shipping           = models.CharField(max_length=50)
    package            = models.CharField(max_length=50)
    origin             = models.CharField(max_length=50)
    price              = models.DecimalField(max_digits=10, decimal_places=2)
    weight             = models.CharField(max_length=150)
    stock              = models.IntegerField(default=0)
    category           = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name
        
class Image(TimeStampModel):
    url     = models.URLField()
    product = models.ForeignKey("Product",on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'