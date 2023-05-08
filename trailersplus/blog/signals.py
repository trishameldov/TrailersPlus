import logging
from pathlib import Path
from subprocess import call

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.images.models import AbstractImage

logger = logging.getLogger(__name__)


def upload_file(server, source, destination):
    cmd = f"unison {source} ssh://trailersplus@{server}/{destination}"
    logger.warning("UPLOADING FILE -> " + cmd)
    call(cmd.split())


@receiver(post_save, sender=AbstractImage)
def save_images(sender, instance, created, **kwargs):
    if settings.SERVER_X and settings.SERVER_Y:
        upload_file(
            settings.SERVER_X,
            str(Path(settings.MEDIA_ROOT)),
            str(Path(settings.MEDIA_ROOT)),
        )
        upload_file(
            settings.SERVER_Y,
            str(Path(settings.MEDIA_ROOT)),
            str(Path(settings.MEDIA_ROOT)),
        )
