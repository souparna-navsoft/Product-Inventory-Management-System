from django.urls import path
from product_inventory_management_system_app import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi



urlpatterns = [
    path('createlistproduct/' , views.ProductCreateListAPIView.as_view() , name='create-list-product'),
    path('updateproduct/<uuid:pk>/' , views.ProductUpdateAPIView.as_view() , name='update-product'),
    path('deleteproduct/<uuid:pk>/', views.ProductDeleteAPIView.as_view() , name='delete-product'),
    path('createliststore/' , views.StoreCreateListAPIView.as_view() , name='create-list-store'),
    path('updatestore/<uuid:pk>/' , views.StoreUpdateAPIView.as_view() , name='update-store'),
    path('deletestore/<uuid:pk>/' , views.StoreDeleteAPIView.as_view() , name='delete-store'),
    path('createlistinventory/' , views.InventoryCreateListAPIView.as_view() , name='create-list-inventory'),
    path('deleteinventory/<int:pk>/' , views.InventoryDeleteAPIView.as_view() , name='delete-inventory'),
    path('createlistuser/' , views.UserCreateListAPIView.as_view() , name='create-list-user'),
    path('updateuser/<int:pk>/' , views.UserUpdateAPIView.as_view() , name='update-user'),
    path('deleteuser/<int:pk>/' , views.UserDeleteAPIView.as_view() , name='delete-user'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/product/export/xlsx/', views.ExportProductToXLSXAPIView.as_view(), name='export_product_xlsx'),
    path('api/product/export/csv/', views.ExportProductToCSVAPIView.as_view(), name='export_product_csv'),
    path('api/product/import/xlsx/', views.ImportProductFromXLSXAPIView.as_view(), name='import_product_xlsx'),
]