from django.urls import path
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
]