from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/needs/', include('needs.urls')),
    path('api/custom_messages/', include('custom_messages.urls')),
    path('api/stats/', include('stats.urls')),
    path('api/seasons/', include('seasons.urls')),
    path('api/news/', include('news.urls')),

    path('api/notices/',include('notices.urls')),
    path('api/payments/',include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)