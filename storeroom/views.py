from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from django.contrib import messages
from utils import IsAdminUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UpdateForm,SearchForm,CteateForm
class StoreRoomView(LoginRequiredMixin,View):
    def get(self, request):
        form=SearchForm()
        products = Product.objects.all()
        if request.GET.get('search'):

                products=products.filter(id=request.GET['search'])
        return render(request, 'storeroom/storeroom.html', {'products':products, 'form':form})


class ProductDetailView(LoginRequiredMixin,View):
    def get(self, request, name):
        product = get_object_or_404(Product, name=name)
        form = UpdateForm()
        return render(request, 'storeroom/storeroom_update.html', {'product': product, 'form': form})


class ProductUpdateView(LoginRequiredMixin,View):
    def post(self,request,product_id):
        form=UpdateForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            obj=get_object_or_404(Product,id=product_id)
            obj.available=cd['available']
            obj.price=cd['price']
            obj.save()
            messages.success(request, 'available updated successfully', 'info')
        return redirect('storeroom:storeroom')

class ProductCreateView(LoginRequiredMixin,View):
    form = CteateForm
    def get(self,request):
        return render(request, 'storeroom/storeroom_craete.html', {'form':self.form})

    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            Product.objects.create(name=cd['name'],description=cd['description'],price=cd['price'],available=cd['available'])
            messages.success(request, 'created successfully', 'info')
        return redirect('storeroom:storeroom')