
from api.endpoints.login.views import RegisterAPIView,CustomTokenObtainPairView
from django.urls import path

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]