# Generated by Django 3.0.11 on 2021-07-02 22:13

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0018_mystore_schema_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailpage',
            name='content',
            field=wagtail.core.fields.StreamField([('product_list', wagtail.core.blocks.StructBlock([('back_to_inventory_text', wagtail.core.blocks.TextBlock(required=False)), ('mail_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('print_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('sale_price_text', wagtail.core.blocks.CharBlock(required=False)), ('found_it_lower_text', wagtail.core.blocks.CharBlock(required=False)), ('get_off_sale_text', wagtail.core.blocks.CharBlock(help_text='Use <off_price> to insert off price automatically. EX. "Get <off_price>$ off" --> "Get 50$ off"', required=False)), ('financing_available_text', wagtail.core.blocks.TextBlock(required=False)), ('schedule_an_appointment_button_text', wagtail.core.blocks.CharBlock(required=False)), ('reserve_trailer_button_text', wagtail.core.blocks.CharBlock(required=False)), ('add_to_cart_button_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_located_at_text', wagtail.core.blocks.CharBlock(required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(required=False)), ('free_delivery_text', wagtail.core.blocks.TextBlock(required=False)), ('why_we_are_appointment_text', wagtail.core.blocks.CharBlock(required=False)), ('specifications_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_details_text', wagtail.core.blocks.CharBlock(required=False)), ('color_text', wagtail.core.blocks.CharBlock(required=False)), ('size_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_text', wagtail.core.blocks.CharBlock(required=False)), ('coupler_text', wagtail.core.blocks.CharBlock(required=False)), ('features_text', wagtail.core.blocks.CharBlock(required=False)), ('clearance_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('tail_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('undercoating_text', wagtail.core.blocks.CharBlock(required=False)), ('dimensions_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_length_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_width_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_height_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_length_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_width_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_width_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_and_brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('empty_weight_text', wagtail.core.blocks.CharBlock(required=False)), ('suspensions_text', wagtail.core.blocks.CharBlock(required=False)), ('brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('construction_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('wall_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('flooring_text', wagtail.core.blocks.CharBlock(required=False)), ('walls_text', wagtail.core.blocks.CharBlock(required=False)), ('nationwide_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_text', wagtail.core.blocks.CharBlock(required=False)), ('roof_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_url_text', wagtail.core.blocks.RichTextBlock(required=False)), ('trailers_reserved', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_sold', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('cta', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('title', wagtail.core.blocks.TextBlock(required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('reserve_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('schedule_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('banner_link_text_top', wagtail.core.blocks.TextBlock(required=False)), ('banner_link_text_bot', wagtail.core.blocks.TextBlock(required=False)), ('banner_link', wagtail.core.blocks.CharBlock(required=False))])), ('recently', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_info', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))])), ('partners', streams.blocks.PartnersBlock()), ('reserve', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(max_length=150, required=False)), ('text', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('schedule', wagtail.core.blocks.StructBlock([('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('form_description', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('policy_accept', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('tnx_message', wagtail.core.blocks.CharBlock(help_text='"Thanks for appointment" page url', max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('appointment_right_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('appointment_right_description', wagtail.core.blocks.TextBlock(required=False)), ('appointment_right_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('list_item', wagtail.core.blocks.RichTextBlock(required=False))])))])), ('appointment', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('item_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item', wagtail.core.blocks.RichTextBlock(required=False))]))), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional; Use <phone> to insert store phone automatically. Ex. "Call us <phone>" --> "Call us <a href=\'tel:+1123442\'>+1123442</a>', required=False))])), ('found_lower', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_website_lower', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_zipcode', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('form_description', wagtail.core.blocks.TextBlock(help_text='Optional', required=False))])), ('additional_message', wagtail.core.blocks.StructBlock([('message_text', wagtail.core.blocks.TextBlock())])), ('trust_pilot_reviews', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('trust_pilot_reviews_horizontal', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('bottom_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('paddings', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailpage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('product_list', wagtail.core.blocks.StructBlock([('back_to_inventory_text', wagtail.core.blocks.TextBlock(required=False)), ('mail_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('print_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('sale_price_text', wagtail.core.blocks.CharBlock(required=False)), ('found_it_lower_text', wagtail.core.blocks.CharBlock(required=False)), ('get_off_sale_text', wagtail.core.blocks.CharBlock(help_text='Use <off_price> to insert off price automatically. EX. "Get <off_price>$ off" --> "Get 50$ off"', required=False)), ('financing_available_text', wagtail.core.blocks.TextBlock(required=False)), ('schedule_an_appointment_button_text', wagtail.core.blocks.CharBlock(required=False)), ('reserve_trailer_button_text', wagtail.core.blocks.CharBlock(required=False)), ('add_to_cart_button_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_located_at_text', wagtail.core.blocks.CharBlock(required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(required=False)), ('free_delivery_text', wagtail.core.blocks.TextBlock(required=False)), ('why_we_are_appointment_text', wagtail.core.blocks.CharBlock(required=False)), ('specifications_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_details_text', wagtail.core.blocks.CharBlock(required=False)), ('color_text', wagtail.core.blocks.CharBlock(required=False)), ('size_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_text', wagtail.core.blocks.CharBlock(required=False)), ('coupler_text', wagtail.core.blocks.CharBlock(required=False)), ('features_text', wagtail.core.blocks.CharBlock(required=False)), ('clearance_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('tail_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('undercoating_text', wagtail.core.blocks.CharBlock(required=False)), ('dimensions_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_length_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_width_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_height_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_length_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_width_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_width_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_and_brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('empty_weight_text', wagtail.core.blocks.CharBlock(required=False)), ('suspensions_text', wagtail.core.blocks.CharBlock(required=False)), ('brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('construction_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('wall_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('flooring_text', wagtail.core.blocks.CharBlock(required=False)), ('walls_text', wagtail.core.blocks.CharBlock(required=False)), ('nationwide_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_text', wagtail.core.blocks.CharBlock(required=False)), ('roof_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_url_text', wagtail.core.blocks.RichTextBlock(required=False)), ('trailers_reserved', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_sold', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('cta', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('title', wagtail.core.blocks.TextBlock(required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('reserve_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('schedule_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('banner_link_text_top', wagtail.core.blocks.TextBlock(required=False)), ('banner_link_text_bot', wagtail.core.blocks.TextBlock(required=False)), ('banner_link', wagtail.core.blocks.CharBlock(required=False))])), ('recently', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_info', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))])), ('partners', streams.blocks.PartnersBlock()), ('reserve', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(max_length=150, required=False)), ('text', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('schedule', wagtail.core.blocks.StructBlock([('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('form_description', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('policy_accept', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('tnx_message', wagtail.core.blocks.CharBlock(help_text='"Thanks for appointment" page url', max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('appointment_right_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('appointment_right_description', wagtail.core.blocks.TextBlock(required=False)), ('appointment_right_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('list_item', wagtail.core.blocks.RichTextBlock(required=False))])))])), ('appointment', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('item_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item', wagtail.core.blocks.RichTextBlock(required=False))]))), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional; Use <phone> to insert store phone automatically. Ex. "Call us <phone>" --> "Call us <a href=\'tel:+1123442\'>+1123442</a>', required=False))])), ('found_lower', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_website_lower', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_zipcode', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('form_description', wagtail.core.blocks.TextBlock(help_text='Optional', required=False))])), ('additional_message', wagtail.core.blocks.StructBlock([('message_text', wagtail.core.blocks.TextBlock())])), ('trust_pilot_reviews', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('trust_pilot_reviews_horizontal', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('bottom_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('paddings', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailpage',
            name='content_es',
            field=wagtail.core.fields.StreamField([('product_list', wagtail.core.blocks.StructBlock([('back_to_inventory_text', wagtail.core.blocks.TextBlock(required=False)), ('mail_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('print_text', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('sale_price_text', wagtail.core.blocks.CharBlock(required=False)), ('found_it_lower_text', wagtail.core.blocks.CharBlock(required=False)), ('get_off_sale_text', wagtail.core.blocks.CharBlock(help_text='Use <off_price> to insert off price automatically. EX. "Get <off_price>$ off" --> "Get 50$ off"', required=False)), ('financing_available_text', wagtail.core.blocks.TextBlock(required=False)), ('schedule_an_appointment_button_text', wagtail.core.blocks.CharBlock(required=False)), ('reserve_trailer_button_text', wagtail.core.blocks.CharBlock(required=False)), ('add_to_cart_button_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_located_at_text', wagtail.core.blocks.CharBlock(required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(required=False)), ('free_delivery_text', wagtail.core.blocks.TextBlock(required=False)), ('why_we_are_appointment_text', wagtail.core.blocks.CharBlock(required=False)), ('specifications_text', wagtail.core.blocks.CharBlock(required=False)), ('trailer_details_text', wagtail.core.blocks.CharBlock(required=False)), ('color_text', wagtail.core.blocks.CharBlock(required=False)), ('size_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_text', wagtail.core.blocks.CharBlock(required=False)), ('coupler_text', wagtail.core.blocks.CharBlock(required=False)), ('features_text', wagtail.core.blocks.CharBlock(required=False)), ('clearance_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('tail_lights_text', wagtail.core.blocks.CharBlock(required=False)), ('undercoating_text', wagtail.core.blocks.CharBlock(required=False)), ('dimensions_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_length_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_width_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_height_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_length_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_width_text', wagtail.core.blocks.CharBlock(required=False)), ('interior_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_height_text', wagtail.core.blocks.CharBlock(required=False)), ('rear_door_width_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_and_brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('empty_weight_text', wagtail.core.blocks.CharBlock(required=False)), ('suspensions_text', wagtail.core.blocks.CharBlock(required=False)), ('brakes_text', wagtail.core.blocks.CharBlock(required=False)), ('construction_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_text', wagtail.core.blocks.CharBlock(required=False)), ('frame_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('wall_centers_text', wagtail.core.blocks.CharBlock(required=False)), ('flooring_text', wagtail.core.blocks.CharBlock(required=False)), ('walls_text', wagtail.core.blocks.CharBlock(required=False)), ('nationwide_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('overall_text', wagtail.core.blocks.CharBlock(required=False)), ('roof_text', wagtail.core.blocks.CharBlock(required=False)), ('axles_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_warranty_text', wagtail.core.blocks.CharBlock(required=False)), ('tires_url_text', wagtail.core.blocks.RichTextBlock(required=False)), ('trailers_reserved', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('trailers_sold', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('cta', wagtail.core.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock()), ('background_image_mobile', wagtail.images.blocks.ImageChooserBlock(required=False)), ('title', wagtail.core.blocks.TextBlock(required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('reserve_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('schedule_button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('banner_link_text_top', wagtail.core.blocks.TextBlock(required=False)), ('banner_link_text_bot', wagtail.core.blocks.TextBlock(required=False)), ('banner_link', wagtail.core.blocks.CharBlock(required=False))])), ('recently', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_info', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))])), ('partners', streams.blocks.PartnersBlock()), ('reserve', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=30, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(max_length=150, required=False)), ('text', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=30, required=False))])), ('schedule', wagtail.core.blocks.StructBlock([('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('form_description', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('policy_accept', wagtail.core.blocks.RichTextBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('tnx_message', wagtail.core.blocks.CharBlock(help_text='"Thanks for appointment" page url', max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('appointment_right_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('appointment_right_description', wagtail.core.blocks.TextBlock(required=False)), ('appointment_right_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('list_item', wagtail.core.blocks.RichTextBlock(required=False))])))])), ('appointment', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('item_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item', wagtail.core.blocks.RichTextBlock(required=False))]))), ('textarea', wagtail.core.blocks.TextBlock(help_text='Optional; Use <phone> to insert store phone automatically. Ex. "Call us <phone>" --> "Call us <a href=\'tel:+1123442\'>+1123442</a>', required=False))])), ('found_lower', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.TextBlock(required=False)), ('placeholder_website_lower', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('form_title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('placeholder_first_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_last_name', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_phone', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_email', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('placeholder_zipcode', wagtail.core.blocks.CharBlock(max_length=55, required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('success_message', wagtail.core.blocks.CharBlock(max_length=999, required=False)), ('form_description', wagtail.core.blocks.TextBlock(help_text='Optional', required=False))])), ('additional_message', wagtail.core.blocks.StructBlock([('message_text', wagtail.core.blocks.TextBlock())])), ('trust_pilot_reviews', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('trust_pilot_reviews_horizontal', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('bottom_title', wagtail.core.blocks.CharBlock(help_text='Use <b>...</b> for red bg', max_length=511, required=False)), ('rating', wagtail.core.blocks.FloatBlock(default=0, max_value=5, min_value=0, required=False)), ('background_grey_color', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('is_my_store_page', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('columns_layout', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('paddings', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], blank=True, null=True),
        ),
    ]
