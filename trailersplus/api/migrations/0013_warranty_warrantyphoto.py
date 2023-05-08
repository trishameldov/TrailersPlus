# Generated by Django 3.0.11 on 2021-10-27 22:40

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_fleet_zip_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=45)),
                ('vin', models.CharField(max_length=21, verbose_name='VIN number')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WarrantyPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.models.image_path)),
                ('warranty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Warranty')),
            ],
        ),
    ]