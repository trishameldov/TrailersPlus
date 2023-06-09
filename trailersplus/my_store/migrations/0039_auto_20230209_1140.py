# Generated by Django 3.0.11 on 2023-02-09 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0038_auto_20230123_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_category',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_category_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_inventory',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_inventory_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_subcategory',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventorypage',
            name='seo_block_subcategory_es',
            field=models.TextField(blank=True, null=True),
        ),
    ]
