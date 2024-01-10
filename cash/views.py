from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from storeroom.models import Product
from django.contrib import messages
# from utils import IsAdminUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
from .forms import CartAddForm, CustomerForm
from .models import Order, OrderItem
from storeroom.forms import SearchForm
from django.core.exceptions import ValidationError

class CashView(LoginRequiredMixin, View):  # notice the colon at the end of this line
    def get(self, request):
        form1 = CartAddForm()
        form2 = SearchForm()
        products = Product.objects.all()
        if request.GET.get('search'):
            products=products.filter(id=request.GET['search'])

        return render(request, 'cash/cash.html', {'products': products, 'form1': form1, 'form2': form2, })


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cash/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if int(form.data['quantity']) > product.available:
            messages.error(request,'availability not enough','warning')
            return redirect('cash:cash')
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('cash:cash')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cash:cart')


class OrderDetailView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'cash/order.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)

        order = Order.objects.create(customer='ali')
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
            obj=Product.objects.get(name=item['product'])
            obj.available-=item['quantity']
            obj.save()
        cart.clear()
        return redirect('cash:order_detail', order.id)
