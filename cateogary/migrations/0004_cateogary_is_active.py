# Generated by Django 4.2.3 on 2023-08-16 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cateogary', '0003_remove_cateogary_is_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='cateogary',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
