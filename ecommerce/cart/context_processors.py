from .models import Cart

def cart(request):
    """
    Context processor to provide cart information to all templates
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    else:
        cart = None
        cart_items_count = 0
    
    return {
        'cart': cart,
        'cart_items_count': cart_items_count
    }