# Generated by Django 4.2.3 on 2023-09-04 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordermanagement', '0003_oreder_item_is_cancelled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oreder_item',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ordermanagement.order'),
        ),
    ]