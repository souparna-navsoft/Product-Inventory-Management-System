from rest_framework import serializers
from .models import Product , Store , Inventory
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'sku' , 'name' , 'color' , 'brand' , 'price' , 'description' , 'reviews']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id' , 'name' , 'address' , 'phone_number' , 'email' , 'rating']

class InventorySerializer(serializers.ModelSerializer):

    # store = StoreSerializer()
    # product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = ['product' , 'store' , 'quantity' , 'last_stocked_date' , 'is_available']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username' , 'first_name' , 'last_name' , 'email' , 'password']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls , user):
        token = super().get_token(user)
        token['username'] = user.username
        return token