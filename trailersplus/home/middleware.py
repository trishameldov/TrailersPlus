import logging
from django.conf import settings
from django.middleware.common import BrokenLinkEmailsMiddleware


class BrokenLinkMiddleware(BrokenLinkEmailsMiddleware):
    def process_response(self, request, response):
        """Send broken link emails for relevant 404 NOT FOUND responses."""
        if response.status_code == 404 and not settings.DEBUG:
            domain = request.get_host()
            path = request.get_full_path()
            referer = request.META.get('HTTP_REFERER', '')

            if not self.is_ignorable_request(request, path, domain, referer):
                ua = request.META.get('HTTP_USER_AGENT', '<none>')
                ip = request.META.get('REMOTE_ADDR', '<none>')
                message = "%slink on %s\nReferrer: %s\nRequested URL: %s\nUser agent: %s\nIP address: %s\n" % (
                    ('INTERNAL ' if self.is_internal_request(domain, referer) else ''),
                    domain, referer, path, ua, ip
                )
                logger = logging.getLogger(__name__)
                logger.warning(message)
        return response
