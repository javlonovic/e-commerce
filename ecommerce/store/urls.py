# store/urls.py

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.product_list, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('save/<int:product_id>/', views.toggle_save_product, name='toggle_save_product'),
    path('saved/', views.saved_products, name='saved_products'),
]