from modeltranslation.translator import TranslationOptions, register

from .models import Category, Post, Tag


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ("title", "excerpt", "body")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)
