from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):

    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    visible = models.BooleanField(default=False)
    storage = models.IntegerField()
    image = models.URLField(max_length=255, null=False, blank=True)
    name = models.CharField(max_length=55)
    ean = models.CharField(max_length=13, null=False, blank=True, db_index=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}"


class Orders(models.Model):

    ORDER_STATUS = [
        ('completed', 'Wysłano'),
        ('in_progress ', 'W realizacji'),
        ('order_accept ', 'Przyjęto zamówienie')
    ]
    status = models.CharField(max_length=18, choices=ORDER_STATUS)
    product_id = models.ManyToManyField(Product, through='Order_item')
    email = models.EmailField(max_length=128)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    post_code = models.CharField(max_length=6)
    city = models.CharField(max_length=64)
    adress = models.CharField(max_length=255)
    country = models.CharField(max_length=32)
    description = models.TextField(max_length=2000, null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.orders} {self.product} Ilość: {self.value}"

