# Generated by Django 3.0.11 on 2021-10-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_lowerprice_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleet',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
