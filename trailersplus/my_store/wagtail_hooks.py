from django.core.cache import cache
from wagtail.core import hooks
import logging

from home.tasks import cache_invalidation_task

logger = logging.getLogger(__name__)

@hooks.register('after_edit_page')
def cache_invalidation_hook(request, page):
    pass
    # logger.warning('--------- STARTING CACHE INVALIDATION ------')
    # if page.live:
    #     logger.warning('Page is live')
    #     logger.warning(f"{page.pk}")
    #     cache_invalidation_task.run(page.pk, page.__class__)
    #     logger.warning('--------- CACHE INVALIDATION FINISHED ------')
    # else:
    #     logger.warning("Page isn't live, task won't be run.")

hooks.register('after_edit_page', cache_invalidation_hook)
