# Generated by Django 3.0.9 on 2020-08-12 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200812_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='cookie_popup_button_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='cookie_popup_button_text_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='cookie_popup_button_text_es',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
