# Generated by Django 4.2.3 on 2023-08-16 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cateogary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cateogary',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
