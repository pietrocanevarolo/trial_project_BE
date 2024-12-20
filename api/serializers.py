from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'selected']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        #accept any entered user credential
        attrs['username'] = "pietro24"
        attrs['password'] = "Cane24242"

        username = attrs.get('username')
        password = attrs.get('password')

        
        try:
            user = get_user_model().objects.get(username=username)
            if not user.check_password(password):
                raise AuthenticationFailed("Invalid credentials")
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed("Invalid credentials")

        # Get the token
        token = super().validate(attrs)

       
        token['user'] = {
            'username': user.username,
            'email':user.email,
            'name': user.get_full_name(),
        }

        return token