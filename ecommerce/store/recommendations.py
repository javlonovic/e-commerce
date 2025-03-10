# store/recommendations.py

from django.db.models import Count
from .models import Product, SavedItem, Category
from cart.models import CartItem

def get_recommended_products(user, product, limit=5):
    """
    Get recommended products based on the current product and user history.
    Uses a simple collaborative filtering approach:
    
    1. First tries to find products that users who viewed/bought this item also liked
    2. Then looks at products in the same category
    3. Finally falls back to popular products if needed
    
    Args:
        user: The current user (or None if anonymous)
        product: The current product being viewed
        limit: Number of recommendations to return
    
    Returns:
        QuerySet of recommended products
    """
    recommended = []
    
    # Get the current product's category
    current_category = product.category
    
    # Start with a base queryset of all products except the current one
    base_queryset = Product.objects.exclude(id=product.id)
    
    if user and user.is_authenticated:
        # 1. Find products that other users who liked this product also liked
        # Get users who saved or bought this product
        users_who_liked = SavedItem.objects.filter(product=product).values_list('user', flat=True)
        users_who_bought = CartItem.objects.filter(product=product).values_list('cart__user', flat=True)
        
        all_interested_users = list(set(list(users_who_liked) + list(users_who_bought)))
        
        if all_interested_users:
            # Find products these users saved or bought
            products_liked_by_similar_users = SavedItem.objects.filter(
                user__in=all_interested_users
            ).exclude(
                product=product
            ).values_list('product', flat=True)
            
            products_bought_by_similar_users = CartItem.objects.filter(
                cart__user__in=all_interested_users
            ).exclude(
                product=product
            ).values_list('product', flat=True)
            
            # Combine these product IDs
            collaborative_recommendations = list(set(
                list(products_liked_by_similar_users) + 
                list(products_bought_by_similar_users)
            ))
            
            if collaborative_recommendations:
                # Get these products
                collab_products = base_queryset.filter(id__in=collaborative_recommendations)
                recommended.extend(list(collab_products)[:limit])
    
    # 2. If we need more recommendations, add products from the same category
    if len(recommended) < limit:
        needed = limit - len(recommended)
        same_category_products = base_queryset.filter(
            category=current_category
        ).exclude(
            id__in=[p.id for p in recommended]
        )
        recommended.extend(list(same_category_products)[:needed])
    
    # 3. If we still need more, add popular products from other categories
    if len(recommended) < limit:
        needed = limit - len(recommended)
        # Count the number of times each product has been saved or added to cart
        saved_counts = SavedItem.objects.values('product').annotate(count=Count('id')).order_by('-count')
        cart_counts = CartItem.objects.values('product').annotate(count=Count('id')).order_by('-count')
        
        # Combine these counts
        product_popularity = {}
        for item in saved_counts:
            product_id = item['product']
            product_popularity[product_id] = item['count']
        
        for item in cart_counts:
            product_id = item['product']
            if product_id in product_popularity:
                product_popularity[product_id] += item['count']
            else:
                product_popularity[product_id] = item['count']
        
        # Sort by popularity
        popular_product_ids = sorted(product_popularity.keys(), 
                                    key=lambda k: product_popularity[k], 
                                    reverse=True)
        
        # Filter out products already in our recommendations
        popular_product_ids = [pid for pid in popular_product_ids 
                              if pid not in [p.id for p in recommended]]
        
        if popular_product_ids:
            popular_products = base_queryset.filter(id__in=popular_product_ids)
            recommended.extend(list(popular_products)[:needed])
    
    # If we still don't have enough, just add random products
    if len(recommended) < limit:
        needed = limit - len(recommended)
        random_products = base_queryset.exclude(
            id__in=[p.id for p in recommended]
        ).order_by('?')
        recommended.extend(list(random_products)[:needed])
    
    return recommended[:limit]