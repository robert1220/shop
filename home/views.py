from django.shortcuts import render
from home.models import Product
from home.models import Category
from django.views.generic.list import ListView

# Create your views here.
class IndexList(ListView):
    model = Product
    template_name = 'home/index.html'

    def get_queryset(self):
        return Product.objects.all().order_by('?')[:9]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.all()
        return context