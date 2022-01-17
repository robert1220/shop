from django.urls import path
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
    path('category/<int:id>', views.ProductList.as_view(), name='list'),
    path('<int:pk>', views.ProductDetail.as_view(), name='detail'),
]