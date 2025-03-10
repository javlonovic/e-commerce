# cart/models.py (add Order models)

from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Existing Cart and CartItem models...

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_CHOICES = (
        ('cash', 'Cash On Delivery'),
        # Add more payment methods as needed
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of purchase
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
    @property
    def total_price(self):
        return self.price * self.quantity

# cart/views.py (add checkout views)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderForm  # We'll create this next

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty. Please add items before checkout.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create order in a transaction to ensure consistency
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                
                # Create order items from cart items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity
                    )
                
                # Clear the cart
                cart.items.all().delete()
                
                messages.success(request, 'Your order has been placed successfully!')
                return redirect('cart:order_success', order_id=order.id)
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if hasattr(request.user, 'profile'):
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': request.user.profile.address,
                'phone': request.user.profile.phone_number,
            }
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    
    return render(request, 'cart/checkout.html', context)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_success.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})

# cart/forms.py

from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'payment_method']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

# cart/urls.py (update)

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]