from django.conf import settings
from django.core.urlresolvers import reverse
from oabutton.apps.bookmarklet.models import OABlockedURL
from oabutton.apps.template_email import TemplateEmail
import hashlib
import time


def send_author_notification(author_email, blocked_url):
    """
    Send the author of a paper notification that his paper was
    blocked. Request for an open link.
    """
    md5hash = hashlib.md5(author_email + blocked_url + time.asctime())
    slug = md5hash.hexdigest()
    record = OABlockedURL.objects.create(slug=slug,
                                         author_email=author_email,
                                         blocked_url=blocked_url)
    record.save()

    oa_free_url = settings.HOSTNAME + reverse('bookmarklet:open_document', kwargs={'slug': slug})

    context = {'blocked_url': blocked_url,
               'oa_free_url': oa_free_url}

    email = TemplateEmail(template='bookmarklet/request_open_version.html',
                          context=context,
                          from_email=settings.OABUTTON_EMAIL,
                          to=[author_email])
    email.send()
    return True


def check_paper(url, slug, created):
    """
    This method checks that the url is readable.

    For now, just ping it with a requests call.
    """
    raise NotImplementedError
