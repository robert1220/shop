from django.contrib import admin
from home.models import Category
from home.models import Product
from home.models import Orders
from home.models import Order_item
from home.models import Unit

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(Order_item)
admin.site.register(Unit)
