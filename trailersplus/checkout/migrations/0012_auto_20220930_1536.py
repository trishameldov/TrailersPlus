# Generated by Django 3.0.11 on 2022-09-30 20:36

import checkout.models.django
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20220822_1528'),
        ('checkout', '0011_auto_20220805_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testinvoice',
            name='trailer',
            field=models.ForeignKey(default=checkout.models.django.default_trailer, on_delete=django.db.models.deletion.PROTECT, to='product.Trailer', verbose_name='Trailer'),
        ),
    ]
