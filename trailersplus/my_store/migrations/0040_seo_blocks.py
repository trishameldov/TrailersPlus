from django.db import migrations
import streams.blocks

def fill_seo_block_fields(apps, schema_editor):
    InventoryPage = apps.get_model('my_store', 'InventoryPage')
    inventory_page = InventoryPage.objects.all().first()
    
    inventory_page.seo_block_category = """
        Browse our $category trailers for sale to find the trailer that's perfect for your business and personal needs. Our trailer dealership in $city, $state, sells durable, built to last $category trailers at factory direct prices. Whether you’re looking for large or small trailers for sale, we want to make sure you get a great deal and that you’re confident in your purchase. Once you find the right $category trailer, give your local TrailersPlus trailer dealership a call to set up an appointment with our certified team.
    """
    inventory_page.seo_block_subcategory = """
        We at TrailersPlus make finding the perfect $sub_category trailer for sale as simple as browsing our online inventory. All of our $sub_category trailers are built to last and come with factory direct price tags. From small trailers for sale to larger types for those big jobs, we have the high-quality inventory you’re looking for. Browse our stock of $sub_category trailers today, and then give our certified team a call to set up an appointment at your local TrailersPlus trailer dealership in $city, $state.
    """
    inventory_page.seo_block_category_es = """
        Explore nuestros trailers de $category a la venta para encontrar el remolque perfecto para sus necesidades de negocio y personales. Nuestro concesionario de Trailers en $city, $state, vende trailers duraderos, construidos para durar $categoría a precios directos de fábrica. Ya sea que esté buscando trailers grandes o pequeños a la venta, queremos asegurarnos de que obtenga una excelente oferta y que tenga confianza en su compra. Una vez que encuentre el trailer de $category correcto, llame a su concesionario de trailers TrailersPlus local para programar una cita con nuestro equipo certificado.
    """
    inventory_page.seo_block_subcategory_es = """
        En TrailersPlus hacemos que encontrar el tráiler perfecto de $sub_category a la venta sea tan simple como navegar por nuestro inventario en línea. Todos nuestros remolques de $sub_category están diseñados para durar y vienen con precios directos de fábrica. Desde pequeños trailers a la venta hasta tipos más grandes para esos grandes trabajos, tenemos el inventario de alta calidad que está buscando. Explore nuestro inventario de trailers de $sub_category hoy y luego llame a nuestro equipo certificado para programar una cita en su concesionario de trailers TrailersPlus local en $city, $state.
    """
    inventory_page.seo_block_inventory = """
        Browse our trailers for sale to find the trailer that's perfect for your business and personal needs. Our trailer dealership in $city, $state, sells durable, built to last trailers at factory direct prices. Whether you’re looking for large or small trailers for sale, we want to make sure you get a great deal and that you’re confident in your purchase. Once you find the right trailer, give your local TrailersPlus trailer dealership a call to set up an appointment with our certified team.
    """
    inventory_page.seo_block_inventory_es = """
        Explore nuestros trailers a la venta para encontrar el remolque perfecto para sus necesidades de negocio y personales. Nuestro concesionario de Trailers en $city, $state, vende trailers duraderos, construidos para durar a precios directos de fábrica. Ya sea que esté buscando trailers grandes o pequeños a la venta, queremos asegurarnos de que obtenga una excelente oferta y que tenga confianza en su compra. Una vez que encuentre el trailer correcto, llame a su concesionario de trailers TrailersPlus local para programar una cita con nuestro equipo certificado.
    """


    inventory_page.save()

def reverse_fill_seo_block_fields(apps, schema_editor):
    InventoryPage = apps.get_model('my_store', 'InventoryPage')
    inventory_page = InventoryPage.objects.all().first()

    inventory_page.seo_block_category = ""
    inventory_page.seo_block_subcategory = ""
    inventory_page.seo_block_category_es = ""
    inventory_page.seo_block_subcategory_es = ""
    inventory_page.seo_block_inventory = ""
    inventory_page.seo_block_inventory_es = ""

    inventory_page.save()

class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0039_auto_20230209_1140'),
    ]

    operations = [
        migrations.RunPython(fill_seo_block_fields, reverse_code=reverse_fill_seo_block_fields)
    ]
