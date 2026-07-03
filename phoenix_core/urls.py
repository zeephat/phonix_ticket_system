"""
URL configuration for phoenix_core project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Panel ya Admin
    path('admin/', admin.site.urls),
    
    # 2. HII NDIO SULUHISHO: Tunafuta neno 'api/' na kuacha wazi ''
    # Hii inafanya app yako ya tickets isomewe moja kwa moja kwenye njia ya kawaida!
    path('', include('tickets.urls')), 
]