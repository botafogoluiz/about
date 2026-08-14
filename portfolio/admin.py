from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Project


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ("title", "is_visible")
    list_filter = ("is_visible",)
