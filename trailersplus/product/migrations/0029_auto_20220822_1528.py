# Generated by Django 3.0.11 on 2022-08-22 20:19

from django.db import migrations, models

def dummy_migration_function(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_sql_20220822_1527'),
    ]

    operations = [
        migrations.RunPython(dummy_migration_function),
    ]