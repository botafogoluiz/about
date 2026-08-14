from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import TranslateAdminMixin

from .models import Project


@admin.register(Project)
class ProjectAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("title", "is_visible")
    list_filter = ("is_visible",)
