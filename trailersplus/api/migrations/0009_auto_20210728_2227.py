# Generated by Django 3.0.11 on 2021-07-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210611_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowerprice',
            name='url',
            field=models.CharField(max_length=250),
        ),
    ]
