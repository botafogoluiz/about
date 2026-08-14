from django.conf import settings


class ForceDefaultLanguageMiddleware:
    """Ignore the browser's Accept-Language header so first-time visitors always
    land on English, regardless of their browser's language settings. Runs
    before LocaleMiddleware. Explicit switches (which set the language cookie
    via the nav's EN/PT-BR links) still take priority over this.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
            request.META["HTTP_ACCEPT_LANGUAGE"] = settings.LANGUAGE_CODE
        return self.get_response(request)
