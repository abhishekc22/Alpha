# Generated by Django 4.2.3 on 2023-08-23 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_offer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='offer',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='coupon',
        ),
    ]
