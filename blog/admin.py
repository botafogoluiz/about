from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import TranslateAdminMixin

from .models import Post, Tag


@admin.register(Post)
class PostAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("title", "status", "published_date")
    list_filter = ("status",)
    search_fields = ("title", "excerpt")
    filter_horizontal = ("tags",)
    ordering = ("-published_date",)
    formfield_overrides = {
        models.TextField: {"widget": CKEditor5Widget(config_name="default")},
    }


@admin.register(Tag)
class TagAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("name", "slug")
