from django.urls import path
from . import views

app_name = 'storeroom'

urlpatterns = [
    path('', views.StoreRoomView.as_view(), name='storeroom'),
    path('create/', views.ProductCreateView.as_view(), name='storeroom_create'),
    path('<str:name>/', views.ProductDetailView.as_view(), name='storeroom_detail'),
    path('update/<int:product_id>/', views.ProductUpdateView.as_view(), name='storeroom_update'),





]
