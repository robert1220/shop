from django.urls import path
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
    path('list/<int:id>', views.ProductList.as_view(), name='list'),
]