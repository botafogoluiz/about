from modeltranslation.translator import TranslationOptions, register

from .models import Post, Tag


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ("title", "excerpt", "body")


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)
