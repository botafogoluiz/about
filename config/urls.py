from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("timeline.urls")),
    path("blog/", include("blog.urls")),
    path("portfolio/", include("portfolio.urls")),
    prefix_default_language=True,
)

# Django serves /media/ directly in every environment, not just DEBUG — see
# the media files note in settings.py.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
