# Generated by Django 4.2.11 on 2024-04-15 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_inventory_management_system_app', '0002_remove_store_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]