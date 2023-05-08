from blog.models import BlogDetailPage
from django.core.management.base import BaseCommand
from home.models import HomePage


class Command(BaseCommand):

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        for post in BlogDetailPage.objects.all():
            post.move(home, pos='last-child')
