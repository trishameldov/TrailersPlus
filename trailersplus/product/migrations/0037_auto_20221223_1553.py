# Generated by Django 3.0.11 on 2022-12-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_auto_20221222_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
