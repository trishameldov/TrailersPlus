# Generated by Django 3.0.11 on 2022-11-23 19:58

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0035_auto_20221101_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorypage',
            name='content',
            field=wagtail.core.fields.StreamField([('banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title_start', wagtail.core.blocks.CharBlock(help_text='Aprox. this text "The best price & selection of trailers in"', max_length=120, required=False)), ('guaranteed_translation', wagtail.core.blocks.CharBlock(max_length=25, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=120, required=False)))])), ('product_list', wagtail.core.blocks.StructBlock([('category_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sort_by_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('price_l_t_h', wagtail.core.blocks.CharBlock(help_text='Price low to high', max_length=30, required=False)), ('price_h_t_l', wagtail.core.blocks.CharBlock(help_text='Price high to low', max_length=30, required=False)), ('size_l_t_h', wagtail.core.blocks.CharBlock(help_text='Size low to high', max_length=30, required=False)), ('size_h_t_l', wagtail.core.blocks.CharBlock(help_text='Size high to low', max_length=30, required=False)), ('sold_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('reserved_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sale_price', wagtail.core.blocks.CharBlock(max_length=20, required=False))])), ('bullets', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=120, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=511, required=False), help_text='Use <store> to insert store name automatically. Ex. "Buy in <store>" --> "Buy in TrailersPlus Warrenton,VA"'))])), ('social_network', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Join The TrailersPlus Community', required=False)), ('text', wagtail.core.blocks.CharBlock(default='Stay Up to Date With the Latest and Greatest', required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock()), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('partners', streams.blocks.PartnersBlock()), ('fleet_sales_banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('bottom_logo', wagtail.images.blocks.ImageChooserBlock(help_text='Optional', required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(help_text='To highlight the word into red please put it inside these tags: <b>…text…</b>', required=False)), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional - <p>', required=False)), ('overlay', wagtail.core.blocks.IntegerBlock(default=2, help_text='Min: 1, Max: 5', max_value=5, min_value=1, required=False)), ('float_left', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('blue_text_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('service_button_text', wagtail.core.blocks.CharBlock(help_text='Optional', max_length=255, required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorypage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title_start', wagtail.core.blocks.CharBlock(help_text='Aprox. this text "The best price & selection of trailers in"', max_length=120, required=False)), ('guaranteed_translation', wagtail.core.blocks.CharBlock(max_length=25, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=120, required=False)))])), ('product_list', wagtail.core.blocks.StructBlock([('category_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sort_by_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('price_l_t_h', wagtail.core.blocks.CharBlock(help_text='Price low to high', max_length=30, required=False)), ('price_h_t_l', wagtail.core.blocks.CharBlock(help_text='Price high to low', max_length=30, required=False)), ('size_l_t_h', wagtail.core.blocks.CharBlock(help_text='Size low to high', max_length=30, required=False)), ('size_h_t_l', wagtail.core.blocks.CharBlock(help_text='Size high to low', max_length=30, required=False)), ('sold_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('reserved_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sale_price', wagtail.core.blocks.CharBlock(max_length=20, required=False))])), ('bullets', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=120, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=511, required=False), help_text='Use <store> to insert store name automatically. Ex. "Buy in <store>" --> "Buy in TrailersPlus Warrenton,VA"'))])), ('social_network', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Join The TrailersPlus Community', required=False)), ('text', wagtail.core.blocks.CharBlock(default='Stay Up to Date With the Latest and Greatest', required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock()), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('partners', streams.blocks.PartnersBlock()), ('fleet_sales_banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('bottom_logo', wagtail.images.blocks.ImageChooserBlock(help_text='Optional', required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(help_text='To highlight the word into red please put it inside these tags: <b>…text…</b>', required=False)), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional - <p>', required=False)), ('overlay', wagtail.core.blocks.IntegerBlock(default=2, help_text='Min: 1, Max: 5', max_value=5, min_value=1, required=False)), ('float_left', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('blue_text_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('service_button_text', wagtail.core.blocks.CharBlock(help_text='Optional', max_length=255, required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorypage',
            name='content_es',
            field=wagtail.core.fields.StreamField([('banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title_start', wagtail.core.blocks.CharBlock(help_text='Aprox. this text "The best price & selection of trailers in"', max_length=120, required=False)), ('guaranteed_translation', wagtail.core.blocks.CharBlock(max_length=25, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=120, required=False)))])), ('product_list', wagtail.core.blocks.StructBlock([('category_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sort_by_title', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('price_l_t_h', wagtail.core.blocks.CharBlock(help_text='Price low to high', max_length=30, required=False)), ('price_h_t_l', wagtail.core.blocks.CharBlock(help_text='Price high to low', max_length=30, required=False)), ('size_l_t_h', wagtail.core.blocks.CharBlock(help_text='Size low to high', max_length=30, required=False)), ('size_h_t_l', wagtail.core.blocks.CharBlock(help_text='Size high to low', max_length=30, required=False)), ('sold_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('reserved_label', wagtail.core.blocks.CharBlock(max_length=20, required=False)), ('sale_price', wagtail.core.blocks.CharBlock(max_length=20, required=False))])), ('bullets', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=120, required=False)), ('bullets', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(max_length=511, required=False), help_text='Use <store> to insert store name automatically. Ex. "Buy in <store>" --> "Buy in TrailersPlus Warrenton,VA"'))])), ('social_network', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Join The TrailersPlus Community', required=False)), ('text', wagtail.core.blocks.CharBlock(default='Stay Up to Date With the Latest and Greatest', required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock()), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('partners', streams.blocks.PartnersBlock()), ('fleet_sales_banner', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('bottom_logo', wagtail.images.blocks.ImageChooserBlock(help_text='Optional', required=False)), ('background_image_alt', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(help_text='To highlight the word into red please put it inside these tags: <b>…text…</b>', required=False)), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional - <p>', required=False)), ('overlay', wagtail.core.blocks.IntegerBlock(default=2, help_text='Min: 1, Max: 5', max_value=5, min_value=1, required=False)), ('float_left', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('blue_text_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('service_button_text', wagtail.core.blocks.CharBlock(help_text='Optional', max_length=255, required=False))]))], blank=True, null=True),
        ),
    ]
