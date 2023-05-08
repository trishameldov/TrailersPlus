from django.core.cache import cache
from django.core.management.base import BaseCommand
from product.models import Location


class Command(BaseCommand):
    def handle(self, *args, **options):
        stores = Location.objects.all()
        for store in stores:
            cache.delete(f'{store.pk}_filters_count_es')
            cache.delete(f'{store.pk}_filters_count_en')
        cache.clear()
