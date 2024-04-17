from django.shortcuts import render
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from .models import Product , Store , Inventory , User
from .serializers import ProductSerializer , StoreSerializer , InventorySerializer , UserSerializer , CustomTokenObtainPairSerializer
from rest_framework import generics , status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from import_export.formats.base_formats import XLSX, CSV
from import_export.resources import modelresource_factory
from .resources import ProductResource
from rest_framework.parsers import MultiPartParser
import tablib




class ProductCreateListAPIView(generics.GenericAPIView):
    product_serializer_class = ProductSerializer
    # permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Get all products',
        operation_description='Retrieve a list of all products'
    )

    def get(self , request , *args , **kwargs):
        product = Product.objects.all()
        product_serializer = self.product_serializer_class(product , many=True)
        context = {
            'total_products' : product.count(),
            'products' : product_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={201: 'Created', 400: 'Bad Request'},
        operation_summary='Create a product',
        operation_description='Create a new product'
    )

    def post(self , request , *args , **kwargs):
        product_serializer = self.product_serializer_class(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data , status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors , status=status.HTTP_400_BAD_REQUEST)            
    
class ProductUpdateAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    product_serializer_class  = ProductSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Update a product',
        operation_description='Update an existing product by providing its ID and new data'
    )

    def put(self , request , *args , **kwargs):
        product = self.get_object()
        product_serializer = self.product_serializer_class(product , data=request.data , partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data , status=status.HTTP_200_OK)
        return Response(product_serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(generics.GenericAPIView):

    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Delete a product',
        operation_description='Delete an existing product by providing its ID'
    )
    
    def delete(self , request , pk , *args , **kwargs):
        product = Product.objects.filter(pk = pk)
        product.delete()
        return Response({'message' : 'Product has been deleted successfully'} , status=status.HTTP_200_OK)
    
class StoreCreateListAPIView(generics.GenericAPIView):
    store_serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Get all stores',
        operation_description='Retrieve a list of all stores'
    )

    def get(self , request , *args , **kwargs):
        store = Store.objects.all()
        store_serializer = self.store_serializer_class(store , many=True)
        context = {
            'total stores' : store.count(),
            'stores' : store_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={201: 'Created', 400: 'Bad Request'},
        operation_summary='Create a store',
        operation_description='Create a new store'
    )
    
    def post(self , request , *args , **kwargs):
        store_serializer = self.store_serializer_class(data=request.data)
        if store_serializer.is_valid():
            store_serializer.save()
            return Response(store_serializer.data , status=status.HTTP_201_CREATED)
        return Response(store_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
class StoreUpdateAPIView(generics.GenericAPIView):
    queryset = Store.objects.all()
    store_serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Update a store',
        operation_description='Update an existing store by providing its ID and new data'
    )

    def put(self , request , *args , **kwargs):
        store = self.get_object()
        store_serializer = self.store_serializer_class(store , data=request.data , partial=True)
        if store_serializer.is_valid():
            store_serializer.save()
            return Response(store_serializer.data , status=status.HTTP_200_OK)
        return Response(store_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
class StoreDeleteAPIView(generics.GenericAPIView):

    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Delete a store',
        operation_description='Delete an existing store by providing its ID'
    )

    def delete(self , request , pk , *args , **kwargs):
        store = Store.objects.filter(pk = pk)
        store.delete()
        return Response({'message' : 'Store has been deleted successfully'} , status=status.HTTP_200_OK)
    
class InventoryCreateListAPIView(generics.GenericAPIView):
    inventory_serializer_class = InventorySerializer
    product_serializer_class = ProductSerializer
    store_serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Get all inventories',
        operation_description='Retrieve a list of all inventories'
    )

    def get(self , request , *args , **kwargs):
        inventory = Inventory.objects.all()
        inventory_serializer = self.inventory_serializer_class(inventory , many=True)
        serialized_inventory = inventory_serializer.data

        product_ids = [item['product'] for item in serialized_inventory]
        product = Product.objects.filter(id__in=product_ids)
        product_serializer = self.product_serializer_class(product , many=True)

        store_ids = [item['store'] for item in serialized_inventory]
        store = Store.objects.filter(id__in=store_ids)
        store_serializer = self.store_serializer_class(store , many=True)


        context = {
            'inventory' : serialized_inventory,
            'products' : product_serializer.data,
            'stores' : store_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={201: 'Created', 400: 'Bad Request'},
        operation_summary='Create a inventory',
        operation_description='Create a new inventory'
    )

    def post(self , request , *args , **kwargs):
        inventory_serializer = self.inventory_serializer_class(data=request.data)
        if inventory_serializer.is_valid():
            inventory_serializer.save()
            return Response(inventory_serializer.data , status=status.HTTP_201_CREATED)
        return Response(inventory_serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class InventoryUpdateAPIView(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    inventory_serializer_class = InventorySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Update an inventory',
        operation_description='Update an existing inventory by providing its ID and new data'
    )

    def put(self , request , *args , **kwargs):
        inventory = self.get_object()
        inventory_serializer = self.inventory_serializer_class(inventory , data=request.data)
        if inventory_serializer.is_valid():
            inventory_serializer.save()
            return Response(inventory_serializer.data , status=status.HTTP_200_OK)
        return Response(inventory_serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class InventoryDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Delete an inventory',
        operation_description='Delete an existing inventory by providing its ID'
    )
    def delete(self , request , pk , *args , **kwargs):
        inventory = Inventory.objects.filter(pk = pk)
        inventory.delete()
        return Response({"message" : "Inventory has been deleted successfully"} , status=status.HTTP_200_OK)
    
class UserCreateListAPIView(generics.GenericAPIView):
    user_serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Get all users',
        operation_description='Retrieve a list of all users'
    )

    def get(self , request , *args , **kwargs):
        user = User.objects.all()
        user_serializer = self.user_serializer_class(user , many=True)
        context = {
            'total_users' : user.count(),
            'users' : user_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={201: 'Created', 400: 'Bad Request'},
        operation_summary='Create a user',
        operation_description='Create a new user'
    )
    
    def post(self , request , *args , **kwargs):
        user_serializer = self.user_serializer_class(data=request.data)
        if user_serializer.is_valid():
            password = user_serializer.validated_data['password']
            user = user_serializer.save()
            user.set_password(password)
            user.save()
            context = {
                'id' : user.id,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'password' : user.password
            }
            return Response(context , status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    user_serializer_class = UserSerializer
    permission_classes = [IsAdminUser,IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Update a user',
        operation_description='Update an existing user by providing its ID and new data'
    )

    def put(self , request , *args , **kwargs):
        user = self.get_object()
        user_serializer = self.user_serializer_class(user , data=request.data , partial=True)
        if user_serializer.is_valid():
            password = user_serializer.validated_data['password']
            user = user_serializer.save()
            user.set_password(password)
            user.save()
            context = {
                'id' : user.id,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'password' : user.password
            }
            return Response(context , status=status.HTTP_200_OK)
        return Response(user.errors , status=status.HTTP_400_BAD_REQUEST)

class UserDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={200: 'OK', 400: 'Bad Request'},
        operation_summary='Delete a user',
        operation_description='Delete an existing user by providing its ID'
    )

    def delete(self , request , pk , *args , **kwargs):
        user = User.objects.filter(pk = pk)
        user.delete()
        return Response({"message" : "User has been deleted successfully"} , status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    token_serializer_class = CustomTokenObtainPairSerializer
    # permission_classes = [IsAuthenticated]


class ExportProductToXLSXAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = None 

    def get(self, request, *args, **kwargs):
        dataset = ProductResource().export(self.get_queryset())
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
        return response

class ExportProductToCSVAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = None  

    def get(self, request, *args, **kwargs):
        dataset = ProductResource().export(self.get_queryset())
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        return response
    
class ImportProductFromXLSXAPIView(generics.GenericAPIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        resource = ProductResource()
        dataset = resource.load(file.read(), format='xlsx')
        result = resource.import_data(dataset, dry_run=True)  

        if not result.has_errors():
            resource.import_data(dataset, dry_run=False) 
            return Response({'success': 'Data imported successfully'}, status=status.HTTP_200_OK)
        else:
            errors = []
            for error in result.rows:
                errors.append({
                    'row': error.row,
                    'errors': dict(error.errors),
                })
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)