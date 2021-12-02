from django.db       import models

from products.models import Product
from users.models    import User
from core.models     import TimeStampModel

class Cart(TimeStampModel):
    quantity = models.IntegerField(default=0)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'