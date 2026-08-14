from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Education, Evidence, Experience, Profile


@admin.register(Profile)
class ProfileAdmin(TranslationAdmin):
    list_display = ("__str__",)


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(TranslationAdmin):
    list_display = ("title", "company_name", "redact_company_name", "start_date", "end_date")
    list_filter = ("redact_company_name",)
    search_fields = ("title", "company_name", "company_description")
    ordering = ("-start_date",)
    inlines = [EvidenceInline]


@admin.register(Education)
class EducationAdmin(TranslationAdmin):
    list_display = ("degree", "institution", "start_date", "end_date")
    ordering = ("-start_date",)
