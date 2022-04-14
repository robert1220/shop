from django.contrib import admin
from home.models import Category
from home.models import Product
from home.models import Orders
from home.models import Order_item
from home.models import Unit
from django.contrib.auth.models import Group, User

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Category)
admin.site.register(Product)
#admin.site.register(Orders)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'email', 'status', 'time_create')

admin.site.register(Order_item)
admin.site.register(Unit)
