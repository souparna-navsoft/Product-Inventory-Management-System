# Generated by Django 4.2.11 on 2024-04-16 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_inventory_management_system_app', '0005_rename_user_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
