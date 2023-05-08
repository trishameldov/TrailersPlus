# Generated by Django 3.0.11 on 2021-12-30 18:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20211229_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image360',
            name='id',
        ),
        migrations.AddField(
            model_name='image360',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='image360',
            name='image_type',
            field=models.CharField(choices=[('EXT360', 'ext360'), ('INT360', 'int360')], default='EXT360', max_length=10),
        ),
    ]