# Generated by Django 4.2.3 on 2023-08-23 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variation', '0001_initial'),
        ('cart', '0004_cartitem_coupon'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'variation')},
        ),
    ]
