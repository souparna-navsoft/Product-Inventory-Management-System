from import_export import resources
from .models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'sku', 'name', 'color', 'brand', 'price', 'description', 'reviews')
