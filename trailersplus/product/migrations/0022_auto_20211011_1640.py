# Generated by Django 3.0.11 on 2021-10-11 21:40

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_add_trailer_trailertranslation_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='pictures',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), null=True, size=None, verbose_name='Pictures list'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['base_type'], name='product_cat_base_ty_b2659d_idx'),
        ),
        migrations.AddIndex(
            model_name='trailer',
            index=models.Index(fields=['model'], name='product_tra_model_acea97_idx'),
        ),
    ]
