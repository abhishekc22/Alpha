# Generated by Django 4.2.3 on 2023-08-16 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cateogary', '0002_cateogary_is_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cateogary',
            name='is_blocked',
        ),
    ]