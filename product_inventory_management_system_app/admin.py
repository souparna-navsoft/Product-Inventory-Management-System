from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product
from .resources import ProductResource

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

admin.site.register(Product, ProductAdmin)
