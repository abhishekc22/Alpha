# Generated by Django 4.2.3 on 2023-08-14 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cateogary', '0001_initial'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('image1', models.ImageField(default='no image  avilable', upload_to='photos/product')),
                ('image2', models.ImageField(default='no image avaiable', upload_to='photos/product')),
                ('image3', models.ImageField(default='no image avaiable', upload_to='photos/product')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('cateogary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cateogary.cateogary')),
            ],
        ),
    ]