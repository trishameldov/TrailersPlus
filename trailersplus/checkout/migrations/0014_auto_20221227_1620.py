# Generated by Django 3.0.11 on 2022-12-27 16:20

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0013_auto_20220930_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutpage',
            name='content',
            field=wagtail.core.fields.StreamField([('checkout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('customer_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('first_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('last_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('company_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('phone_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('email_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('payment_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('billing_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('city_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('state_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('zip_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('card_number_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('cvv_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('expiry_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('i_accept_policy_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('return_refund_text', wagtail.core.blocks.CharBlock(max_length=175, required=False))])), ('confirmation_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('pay_now_button_text', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('form_error_message', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('back_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('continue_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('right_trailer_block', wagtail.core.blocks.StructBlock([('sale_price_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('financing_available_from_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('tax_changes_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('delivery_rules', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('located_at_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('shipping_quote', wagtail.core.blocks.CharBlock(max_length=70, required=False))])), ('before_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('after_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('minutes_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('seconds_text', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_text', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutpage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('checkout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('customer_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('first_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('last_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('company_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('phone_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('email_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('payment_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('billing_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('city_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('state_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('zip_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('card_number_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('cvv_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('expiry_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('i_accept_policy_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('return_refund_text', wagtail.core.blocks.CharBlock(max_length=175, required=False))])), ('confirmation_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('pay_now_button_text', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('form_error_message', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('back_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('continue_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('right_trailer_block', wagtail.core.blocks.StructBlock([('sale_price_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('financing_available_from_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('tax_changes_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('delivery_rules', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('located_at_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('shipping_quote', wagtail.core.blocks.CharBlock(max_length=70, required=False))])), ('before_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('after_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('minutes_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('seconds_text', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_text', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutpage',
            name='content_es',
            field=wagtail.core.fields.StreamField([('checkout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('customer_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('first_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('last_name_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('company_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('phone_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('email_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('payment_info_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('billing_address_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('city_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('state_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('zip_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('card_number_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('cvv_code_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('expiry_placeholder', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('i_accept_policy_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('return_refund_text', wagtail.core.blocks.CharBlock(max_length=175, required=False))])), ('confirmation_form', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('pay_now_button_text', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('form_error_message', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('back_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('continue_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('right_trailer_block', wagtail.core.blocks.StructBlock([('sale_price_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('financing_available_from_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('tax_changes_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('delivery_rules', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('located_at_text', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('get_direction_text', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('shipping_quote', wagtail.core.blocks.CharBlock(max_length=70, required=False))])), ('before_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('after_time_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('minutes_text', wagtail.core.blocks.CharBlock(max_length=255, required=False)), ('seconds_text', wagtail.core.blocks.CharBlock(max_length=255, required=False))])), ('long_text', wagtail.core.blocks.StructBlock([('textarea', wagtail.core.blocks.TextBlock(required=False))]))], blank=True, null=True),
        ),
    ]
