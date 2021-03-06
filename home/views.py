import decimal
from django.shortcuts import render
from django.shortcuts import redirect
from home.models import Product
from home.models import Category
from home.models import Orders
from home.models import Order_item
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_list_or_404
from django.shortcuts import Http404
from django.views import View
from home.forms import ShoppingCartOrderForm
# Create your views here.

class ShoppingCart(View):

    def _get_session_cart_to_dict(self, request):
        if not request.session.get('cart'):
            request.session['cart'] = {}
        sesion_cart = dict(request.session.get('cart'))
        return sesion_cart

    def _add_cart_item(self, request):
        quantity = request.POST.get('product_quantity')
        id = request.POST.get('id_product')
        sesion_cart = self._get_session_cart_to_dict(request)
        if sesion_cart.get(id):
            quantity = int(quantity) + int(sesion_cart.get(id))
            if Product.objects.only('storage').filter(id=id, storage__lt=quantity):
                return redirect('home:cart')
        sesion_cart[id] = quantity
        request.session['cart'] = sesion_cart
        return redirect('home:cart')

    def _update_cart(self, request):
        quantity = request.POST.get('product_quantity')
        id = request.POST.get('id_product')
        if Product.objects.only('storage').filter(id=id, storage__lt=quantity):
            return redirect('home:cart')
        sesion_card = dict(request.session.get('cart'))
        sesion_card[id] = quantity
        request.session['cart'] = sesion_card
        return redirect('home:cart')

    def _del_cart_item(self, request):
        cart_item_to_del = request.POST.get('id_product')
        session_card = dict(request.session.get('cart'))
        session_card.pop(cart_item_to_del)
        request.session['cart'] = session_card
        return redirect('home:cart')

    def _total_sum(self, cart_product):
        total = decimal.Decimal()
        for cart in cart_product:
            total += cart[2]
        return total

    def _bulid_cart(self, products, sess):
        cart_product = []
        for product in products:
            cart_product.append(
                [
                    product, sess[str(product.pk)],
                    decimal.Decimal(sess[str(product.pk)]) * product.price
                ]
            )
        return cart_product

    def _generate_cart(self, session_cart):
        cart = {}
        id_to_query_sql = list(session_cart)
        products = Product.objects.all().filter(pk__in = id_to_query_sql)
        cart['cart_product'] = self._bulid_cart(products,session_cart)
        cart['total_sum'] = self._total_sum(cart['cart_product'])
        return cart

    def _order(self, request):
        items = dict(request.session.get('cart'))
        form = ShoppingCartOrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Orders.objects.create(
                status='order_accept',
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                post_code=data.get('post_code'),
                phone_number=data.get('phone_number'),
                city=data.get('city'),
                adress=data.get('adress'),
                country=data.get('country'),
                description=data.get('descryption')
            )
            for id, value in items.items():
                Order_item.objects.create(
                    product=Product.objects.all().get(pk=id),
                    orders=order,
                    value=value
                )
            request.session.clear()
            return redirect('home:cart')

        session_cart = self._get_session_cart_to_dict(request)
        cart = self._generate_cart(session_cart)
        how_many_items_in_cart = self.how_many_items_it_is_in_cart(request)
        return render(
            request,
            'home/cart.html'
            , context={
                'menu': Category.objects.only('name'),
                'cart_product': cart['cart_product'],
                'total': cart['total_sum'],
                'form': form,
                'how_many_items_in_cart': how_many_items_in_cart,
            }
        )

    def how_many_items_it_is_in_cart(self, request):
        session_cart = self._get_session_cart_to_dict(request)
        values_cart = [int(i) for i in session_cart.values()]
        sum_items_in_cart = sum(values_cart)
        return sum_items_in_cart

    def post(self, request):
        if request.POST.get('operation') == 'delete_item_cart':
            return self._del_cart_item(request)
        elif request.POST.get('operation') == 'update_item_cart':
            return self._update_cart(request)
        elif request.POST.get('operation') == 'add_to_cart':
            return self._add_cart_item(request)
        elif request.POST.get('operation') == 'order_item':
            return self._order(request)
        else:
            raise Http404()

    def get(self, request):
        session_cart = self._get_session_cart_to_dict(request)
        cart = self._generate_cart(session_cart)
        how_many_items_in_cart = self.how_many_items_it_is_in_cart(request)
        form = ShoppingCartOrderForm()
        return render(
           request,
           'home/cart.html'
           ,context={
               'menu':Category.objects.only('name'),
                'cart_product': cart['cart_product'],
                'total': cart['total_sum'],
                'form':form,
                'how_many_items_in_cart':how_many_items_in_cart,
           }
       )

#Disabled
class Order(View):
    def post(self, request):
        items = dict(request.session.get('cart'))
        form = ShoppingCartOrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            order = Orders.objects.create(
                status ='order_accept',
                email = data.get('email'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                post_code = data.get('post_code'),
                phone_number = data.get('phone_number'),
                city = data.get('city'),
                adress = data.get('adress'),
                country = data.get('country'),
                description = data.get('descryption')
            )
            for id, value in items.items():
                Order_item.objects.create(
                    product = Product.objects.all().get(pk=id),
                    orders = order,
                    value = value
            )
            request.session.clear()
            return render(request,'home/order.html', context = {'menu':Category.objects.only('name')})

    def get(self, request):
        form = ShoppingCartOrderForm()
        return render(request,'home/order.html', context = {'menu':Category.objects.only('name'), 'form':form})


class IndexList(ListView):
    model = Product
    template_name = 'home/index.html'

    def get_queryset(self):
        return Product.objects.only('price', 'image', 'name' ).order_by('?')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        context['how_many_items_in_cart'] = ShoppingCart().how_many_items_it_is_in_cart(self.request)
        return context

class ProductList(ListView):
    model = Product
    template_name = 'home/product_list.html'
    paginate_by = 2

    def get_queryset(self):
        product_list = get_list_or_404(Product.objects.all().filter(category_id=self.kwargs.get('id')))
        return product_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        context['how_many_items_in_cart'] = ShoppingCart().how_many_items_it_is_in_cart(self.request)
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'home/product_detail.html'

    def post(self, request, *args, **kwargs):
        return redirect('home:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Category.objects.only('name')
        context['how_many_items_in_cart'] = ShoppingCart().how_many_items_it_is_in_cart(self.request)
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(DetailView, self).render_to_response(context, **response_kwargs)
        return response
