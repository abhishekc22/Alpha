# Generated by Django 4.2.3 on 2023-09-04 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_delete_offer_remove_cartitem_coupon'),
        ('ordermanagement', '0004_alter_oreder_item_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupon'),
        ),
    ]