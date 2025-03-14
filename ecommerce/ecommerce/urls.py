# ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth URLs
    path('accounts/', include('allauth.urls')),  # For Google authentication
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),  # Favicon route
]

# Add static and media URL patterns for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)