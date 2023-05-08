# Generated by Django 3.0.11 on 2022-12-12 22:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_warranty_photo_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_zipcode', models.CharField(max_length=5)),
                ('distances', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]