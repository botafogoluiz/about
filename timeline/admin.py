from django.contrib import admin
from django.http import HttpResponseNotAllowed, JsonResponse
from django.urls import path
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import TranslateAdminMixin
from core.ai_summary import generate_profile_summary

from .models import Education, Evidence, Experience, Language, Profile


@admin.register(Profile)
class ProfileAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("__str__",)
    change_form_template = "admin/core/profile_change_form.html"

    def get_urls(self):
        custom = [
            path(
                "auto-generate-summary/",
                self.admin_site.admin_view(self.auto_generate_summary_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_auto_generate_summary",
            ),
        ]
        return custom + super().get_urls()

    def auto_generate_summary_view(self, request):
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        try:
            summaries = generate_profile_summary()
        except Exception as exc:  # anthropic/network errors -> surface to the admin UI
            return JsonResponse({"error": str(exc)}, status=502)
        return JsonResponse(summaries)


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("title", "company_name", "redact_company_name", "start_date", "end_date")
    list_filter = ("redact_company_name",)
    search_fields = ("title", "company_name", "company_description")
    ordering = ("-start_date",)
    inlines = [EvidenceInline]


@admin.register(Education)
class EducationAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("degree", "institution", "start_date", "end_date")
    ordering = ("-start_date",)


@admin.register(Language)
class LanguageAdmin(TranslateAdminMixin, TranslationAdmin):
    list_display = ("name", "proficiency")
    ordering = ("-proficiency",)
