from django.shortcuts import render
from home.models import Product
from home.models import Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_list_or_404

# Create your views here.
class IndexList(ListView):
    model = Product
    template_name = 'home/index.html'

    def get_queryset(self):
        return Product.objects.only('price', 'image', 'name' ).order_by('?')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        return context

class ProductList(ListView):
    model = Product
    template_name = 'home/product_list.html'
    paginate_by = 5

    def get_queryset(self):
        product_list = get_list_or_404(Product.objects.all().filter(category_id=self.kwargs.get('id')))
        return product_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'home/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        return context