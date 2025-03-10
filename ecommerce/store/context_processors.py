from .models import Category

def categories(request):
    """
    Context processor to provide categories list to all templates
    """
    return {
        'categories': Category.objects.all()
    }