from django.db import migrations

def migrate_murray_to_americanfork(apps, schema_editor):
    Location = apps.get_model('product', 'Location')
    try:
        loc = Location.objects.get(store_city="Murray")
    except Location.DoesNotExist:
        loc = Location.objects.get(store_city="American Fork")
    else:
        loc.store_city = "American Fork"
        loc.store_name = "TrailersPlus American Fork"
        loc.save()
        ms = loc.pages.first()
        ms.slug = "American_Fork"
        ms.slug_en = "American_Fork"
        ms.slug_es = "American_Fork"
        ms.title = "American Fork"
        ms.title_en = "American Fork"
        ms.title_es = "American Fork"
        ms.save()

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20220822_1528'),
    ]

    operations = [
        migrations.RunPython(migrate_murray_to_americanfork),
    ]