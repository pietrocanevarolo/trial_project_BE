from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('api.endpoints.login.urls')),
    path('', include('api.endpoints.product.urls')),
    ]