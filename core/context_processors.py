from django.conf import settings
from django.urls import translate_url


def language_urls(request):
    """Current page's URL translated into every available language, for the nav's language switcher."""
    return {
        "language_urls": {code: translate_url(request.path, code) for code, name in settings.LANGUAGES},
    }
