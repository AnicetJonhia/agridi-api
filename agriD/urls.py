from django.contrib import admin
from django.urls import path, include

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
]
