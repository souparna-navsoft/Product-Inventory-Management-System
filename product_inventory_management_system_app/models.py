from django.db import models
from django.contrib.auth.models import User
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    sku = models.CharField(max_length=50 , unique=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=50 , decimal_places=2)
    description = models.TextField()
    reviews = models.TextField()

class Store(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    rating = models.DecimalField(max_digits=50 , decimal_places=2)

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    last_stocked_date = models.DateField()
    is_available = models.BooleanField(default=True)

