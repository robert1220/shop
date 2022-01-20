import decimal

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from home.models import Product
from home.models import Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_list_or_404
from django.views import View
# Create your views here.

class ShoppingCart(View):

    def _add_cart_item(self, request):
        quantity = request.POST.get('product_quantity')
        id = request.POST.get('id_product')
        update = request.POST.get('update')
        print(update)
        query = render(request, 'home/cart_redirect.html')
        if request.COOKIES.get(id) and not update:
            quantity = int(quantity) + int(request.COOKIES.get(id))
            if Product.objects.only('storage').filter(id=id, storage__lt=quantity):
                return redirect('home:cart')
        query.set_cookie(id, quantity)
        return query

    def _del_card_item(self, request):
        cookie_to_del = request.POST.get('del_id')
        query = render(request,'home/cart_redirect.html')
        query.delete_cookie(cookie_to_del)
        return query

    def _total_sum(self, cart_product):
        total = decimal.Decimal()
        for cart in cart_product:
            total += cart[2]
        return total

    def _del_csrf_token_from_cookie(self, cookie_with_csrf):
        cookie_clear = {}
        cookie_clear.update(cookie_with_csrf)
        cookie_clear.pop('csrftoken')
        return cookie_clear

    def _bulid_card(self, products, cookie_with_not_csrf):
        cart_product = []
        for product in products:
            cart_product.append(
                [
                    product, cookie_with_not_csrf[str(product.pk)],
                    decimal.Decimal(cookie_with_not_csrf[str(product.pk)]) * product.price
                ]
            )
        return cart_product

    def post(self, request):
        if request.POST.get('del_id'):
            return ShoppingCart._del_card_item(self, request)
        else:
            return ShoppingCart._add_cart_item(self, request)

    def get(self, request):
        id_to_query_sql = []
        cookie = ShoppingCart._del_csrf_token_from_cookie(self,request.COOKIES)
        id_to_query_sql.extend(cookie)
        products = Product.objects.all().filter(pk__in=id_to_query_sql)
        cart_product = ShoppingCart._bulid_card(self,products,cookie)
        total_sum_cart = ShoppingCart._total_sum(self,cart_product)

        return render(
           request,
           'home/cart.html'
           ,context={
               'menu':Category.objects.only('name'),
               'cart_product':cart_product,
               'total':total_sum_cart
           }
       )

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
        #context['undo'] = f"category/{self.kwargs.get('id')}"
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'home/product_detail.html'

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        return redirect('home:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        #context['shoping_cart_form'] = ShoppingCartAddForm()
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(DetailView, self).render_to_response(context, **response_kwargs)
        #response.set_cookie('sort_on', 67)
        #print(self.request.COOKIES.get('sort_on'))
        #foo(response)
        return response
