# Generated by Django 5.2.3 on 2025-07-14 12:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('honey', '0005_alter_beeproduct_price_alter_beeproduct_quantity_and_more'),
        ('shop', '0007_rename_cartitem_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='CartItem',
        ),
    ]
