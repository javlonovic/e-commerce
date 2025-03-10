# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Product, SavedItem
from .recommendations import get_recommended_products
def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'store/product_list.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Get recommended products using our recommendation system
    recommended_products = get_recommended_products(request.user, product, limit=5)
    
    # Check if product is in user's saved items
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedItem.objects.filter(user=request.user, product=product).exists()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommended_products': recommended_products,
        'is_saved': is_saved
    })
@login_required
def toggle_save_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    saved_item, created = SavedItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        saved_item.delete()
    
    return redirect('store:product_detail', slug=product.slug)

@login_required
def saved_products(request):
    saved_items = SavedItem.objects.filter(user=request.user)
    return render(request, 'saved/saved_items.html', {'saved_items': saved_items})