from django.db import migrations

def populate_podium_fields(apps, schema):
    """Populates the podium_id and podium_text_number of Location objects."""
    Location = apps.get_model('product', 'Location')

    podium_ids = {
        'TRPL02': 223204,
        'TRPL04': 223206,
        'TRPL05': 223208,
        'TRPL06': 223207,
        'TRPL07': 223205,
        'TRPL09': 223212,
        'TRPL10': 223211,
        'TRPL13': 223210,
        'TRPL15': 223213,
        'TRPL18': 223209,
        'TRPL22': 223214,
        'TRPL24': 223215,
        'TRPL25': 223216,
        'TRPL26': 223217,
        'TRPL27': 223218,
        'TRPL28': 223221,
        'TRPL29': 223224,
        'TRPL30': 223220,
        'TRPL31': 223223,
        'TRPL32': 223222,
        'TRPL33': 223228,
        'TRPL34': 223229,
        'TRPL35': 223226,
        'TRPL36': 223227,
        'TRPL37': 223225,
        'TRPL38': 223230,
        'TRPL39': 223234,
        'TRPL40': 223233,
        'TRPL41': 223231,
        'TRPL42': 223232,
        'TRPL43': 223400,
        'TRPL44': 223404,
        'TRPL45': 223401,
        'TRPL46': 223403,
        'TRPL47': 223402,
        'TRPL48': 223407,
        'TRPL49': 223406,
        'TRPL50': 223405,
        'TRPL51': 223408,
        'TRPL52': 223409,
        'TRPL53': 223411,
        'TRPL54': 223410,
        'TRPL55': 223414,
        'TRPL56': 223413,
        'TRPL57': 223412,
        'TRPL58': 223419,
        'TRPL59': 223417,
        'TRPL60': 223418,
        'TRPL61': 223416,
        'TRPL62': 223415,
        'TRPL63': 223421,
        'TRPL64': 223420,
        'TRPL65': 223422,
        'TRPL66': 223423,
        'TRPL67': 223424,
        'TRPL68': 223427,
        'TRPL69': 223429,
        'TRPL70': 223426,
        'TRPL71': 223428,
        'TRPL72': 223425,
        'TRPL73': 223432,
        'TRPL75': 223431,
        'TRPL76': 223434,
        'TRPL77': 223430,
        'TRPL78': 223433,
        'TRPL79': 223439,
        'TRPL80': 223436,
        'TRPL81': 223438,
        'TRPL82': 223435,
        'TRPL83': 223437,
        'TRPL84': 223440,
        'TRPL85': 223442,
        'TRPL86': 223441,
        'TRPL87': 223445,
        'TRPL88': 223446,
        'TRPL89': 232083,
        'TRPL90': 271472,
        'TRPL91': 271681,
        'TRPL92': 280033,
        'TRPL93': 281430,
    }

    podium_numbers = {
        'TRPL83': '(234) 262-9451',
        'TRPL56': '(505) 589-3452',
        'TRPL30': '(740) 640-6412',
        'TRPL88': '(920) 507-5454',
        'TRPL04': '(770) 746-6517',
        'TRPL63': '(661) 384-8075',
        'TRPL89': '(409) 209-8868',
        'TRPL69': '(406) 380-4787',
        'TRPL29': '(816) 495-3110',
        'TRPL92': '(423) 761-8014',
        'TRPL18': '(501) 382-1005',
        'TRPL85': '(307) 314-0341',
        'TRPL75': '(304) 938-0797',
        'TRPL73': '(423) 540-1938',
        'TRPL36': '(360) 234-3108',
        'TRPL82': '(513) 866-2581',
        'TRPL87': '(936) 227-4266',
        'TRPL65': '(719) 745-7896',
        'TRPL79': '(614) 335-9302',
        'TRPL06': '(501) 550-3747',
        'TRPL62': '(720) 782-2635',
        'TRPL78': '(515) 454-2095',
        'TRPL64': '(910) 631-6947',
        'TRPL60': '(925) 666-2545',
        'TRPL34': '(541) 576-8627',
        'TRPL42': '(805) 572-7735',
        'TRPL49': '(970) 579-4790',
        'TRPL33': '(559) 245-1320',
        'TRPL24': '(817) 409-7351',
        'TRPL35': '(408) 790-1465',
        'TRPL57': '(970) 660-6142',
        'TRPL51': '(406) 295-6228',
        'TRPL46': '(281) 241-1602',
        'TRPL47': '(208) 213-7713',
        'TRPL68': '(317) 548-6136',
        'TRPL84': '(254) 277-1712',
        'TRPL40': '(928) 662-5871',
        'TRPL31': '(619) 505-3873',
        'TRPL02': '(702) 747-6369',
        'TRPL70': '(762) 240-2088',
        'TRPL22': '(615) 882-1328',
        'TRPL15': '(205) 984-3442',
        'TRPL71': '(208) 670-8269',
        'TRPL55': '(336) 872-2759',
        'TRPL07': '(530) 456-4417',
        'TRPL44': '(209) 457-7117',
        'TRPL59': '(502) 747-9341',
        'TRPL26': '(360) 551-4726',
        'TRPL52': '(541) 800-1833',
        'TRPL58': '(763) 401-8226',
        'TRPL90': '(317) 886-1641',
        'TRPL81': '(724) 571-4883',
        'TRPL09': '(208) 273-9317',
        'TRPL61': '(757) 859-0813',
        'TRPL45': '(801) 877-1598',
        'TRPL32': '(405) 554-3777',
        'TRPL72': '(402) 532-1889',
        'TRPL91': '(321) 384-6050',
        'TRPL77': '(541) 303-9127',
        'TRPL13': '(707) 893-9786',
        'TRPL39': '(480) 933-6582',
        'TRPL28': '(503) 966-9373',
        'TRPL37': '(208) 214-4768',
        'TRPL27': '(909) 550-6886',
        'TRPL05': '(541) 283-1592',
        'TRPL50': '(775) 526-3060',
        'TRPL48': '(314) 266-0744',
        'TRPL25': '(503) 479-4142',
        'TRPL67': '(512) 572-3618',
        'TRPL76': '(805) 572-7895',
        'TRPL66': '(318) 531-6161',
        'TRPL38': '(417) 202-4519',
        'TRPL80': '(253) 321-1952',
        'TRPL93': '(239) 572-9768',
        'TRPL54': '(520) 502-7272',
        'TRPL10': '(918) 203-8392',
        'TRPL86': '(208) 812-5790',
        'TRPL43': '(540) 889-3533',
        'TRPL41': '(870) 410-4142',
        'TRPL53': '(316) 800-5795',
    }


    for location in Location.objects.all():
        if location.store_id in podium_ids.keys():
            location.podium_id = podium_ids[location.store_id]
        
        if location.store_id in podium_numbers.keys():
            location.podium_text_number = podium_numbers[location.store_id]

        location.save()

def make_many_reviews(apps, schema):
    """
        Adds the Trailer object in ProductReviews.product to the
        many-to-many relationship in  ProductReviews.products
    """
    ProductReviews = apps.get_model('api', 'ProductReviews')

    for review in ProductReviews.objects.all():
        if review.product is not None:
            review.products.add(review.product)

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_auto_20230120_1127'),
    ]

    operations = [
        migrations.RunPython(populate_podium_fields)
    ]
