# Generated by Django 3.0.11 on 2022-12-15 17:17

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_create_points_for_locations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
