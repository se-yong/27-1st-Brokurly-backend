from django.db       import models

from products.models import Product
from users.models    import User
from core.models     import TimeStampModel

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_status'

    def __str__(self):
        return self.status

class Order(TimeStampModel):
    order_number = models.CharField(max_length=150)
    users        = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.order_number

class OrderItemsStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_items_status'

    def __str__(self):
        return self.status

class OrderItem(TimeStampModel):
    tracking_number    = models.CharField(max_length=200,null=True)
    quantity           = models.IntegerField()
    order              = models.ForeignKey('Order', on_delete=models.CASCADE)
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_items_status = models.ForeignKey('OrderItemsStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'
