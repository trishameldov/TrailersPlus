# Generated by Django 3.0.11 on 2022-07-21 20:11

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0022_auto_20220711_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='statepage',
            name='content',
            field=wagtail.core.fields.StreamField([('product_list', wagtail.core.blocks.StructBlock([('main_section_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('filter_title', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('filter_location', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('filter_types', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('filter_length', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('filter_price', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('close_filter', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_available', wagtail.core.blocks.TextBlock(required=False)), ('trailers_special', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_reserved', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_sold', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('no_trailers_available', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('additional_message', wagtail.core.blocks.StructBlock([('message_text', wagtail.core.blocks.TextBlock())])), ('social_icons_banner', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Join The TrailersPlus Community', required=False)), ('text', wagtail.core.blocks.CharBlock(default='Stay Up to Date With the Latest and Greatest', required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock()), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('partners', streams.blocks.PartnersBlock())], blank=True, null=True),
        ),
    ]
