from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin

from .models import Category, Post, Tag


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ("title", "category", "status", "published_date")
    list_filter = ("status", "category")
    search_fields = ("title", "excerpt")
    filter_horizontal = ("tags",)
    ordering = ("-published_date",)
    formfield_overrides = {
        models.TextField: {"widget": CKEditor5Widget(config_name="default")},
    }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ("name", "slug")
