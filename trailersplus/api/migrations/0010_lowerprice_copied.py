# Generated by Django 3.0.11 on 2021-09-02 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210728_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='lowerprice',
            name='copied',
            field=models.BooleanField(default=False),
        ),
    ]
