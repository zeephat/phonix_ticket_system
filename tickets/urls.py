from django.urls import path
from . import views

urlpatterns = [
    # Ukurasa mkuu wa kutafuta na kuona orodha ya mabasi
    path('', views.tafuta_mabasi_view, name='orodha_mabasi'),
    
    # API Endpoint ya kuchata na backend wakati wa kulipia viti
    path('api/pay/', views.kamilisha_malipo_api, name='kamilisha_malipo_api'),

    path('makampuni/register/', views.sajili_kampuni_view, name='sajili_kampuni'),
]