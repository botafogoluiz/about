from modeltranslation.translator import TranslationOptions, register

from .models import Education, Evidence, Experience, Language, Profile


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ("summary",)


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = ("title", "company_description", "description")


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = ("institution", "degree", "field_of_study", "description")


@register(Evidence)
class EvidenceTranslationOptions(TranslationOptions):
    fields = ("caption",)


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)
