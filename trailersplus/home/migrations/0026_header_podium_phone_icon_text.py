# Generated by Django 3.0.11 on 2023-01-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20210311_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='podium_phone_icon_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]