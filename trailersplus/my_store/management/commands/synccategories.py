from django.core.management.base import BaseCommand
from django.db.models import Q
from my_store.models import Category
from product.models.django import CategoryMap, Trailer


class Command(BaseCommand):

    def handle(self, *args, **options):
        # ### CARGO #####
        cargo = Category.objects.filter(
            category_map__isnull=True, web_category__startswith="Enc"
        ).exclude(web_category__endswith="ATV").update(
            category_map=CategoryMap.objects.get(slug="Cargo")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{cargo} objects updated."
        ))

        # ### UTILITY #####
        utility = Category.objects.filter(
            category_map__isnull=True,
            web_category__startswith="Flt"
        ).exclude(
            web_category__endswith="CC"
        ).exclude(
            web_category__endswith="ATV"
        ).exclude(
            web_category__endswith="Flt7TA"
        ).update(
            category_map=CategoryMap.objects.get(slug="Utility")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{utility} objects updated."
        ))

        # ### HAULER #####
        hauler = Category.objects.filter(category_map__isnull=True).filter(
            Q(web_category__startswith="CC") | Q(web_category__startswith="Flt7TA")
        ).update(
            category_map=CategoryMap.objects.get(slug="Hauler")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{hauler} objects updated."
        ))

        # ### AVT #####
        avt = Category.objects.filter(
            category_map__isnull=True, web_category__endswith="ATV"
        ).update(category_map=CategoryMap.objects.get(slug="ATV"))
        self.stdout.write(self.style.SUCCESS(
            f"{avt} objects updated."
        ))

        # ### DUMP #####
        dump = Category.objects.filter(
            category_map__isnull=True, web_category__startswith="Dump"
        ).exclude(
            Q(web_category__endswith="CC") | Q(web_category__endswith="ATV")
        ).update(
            category_map=CategoryMap.objects.get(slug="Dump")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{dump} objects updated."
        ))

        # ### EQUIPMENT #####
        equipment = Category.objects.filter(category_map__isnull=True).filter(
            Q(web_category__startswith="Eqp") | Q(base_type__startswith="CO7X18") | Q(base_type__startswith="CO7X20")
        ).exclude(
            Q(base_type__endswith="CO7X18") | Q(base_type__endswith="ATV") | Q(web_category="EqpGN")
        ).update(
            category_map=CategoryMap.objects.get(slug="Equipment")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{equipment} objects updated."
        ))

        # ### GOOSENECK #####
        gooseneck = Category.objects.filter(category_map__isnull=True, web_category="EqpGN").update(
            category_map=CategoryMap.objects.get(slug="Gooseneck")
        )
        self.stdout.write(self.style.SUCCESS(
            f"{gooseneck} objects updated."
        ))
