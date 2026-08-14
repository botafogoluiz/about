import json

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.urls import path
from django_ckeditor_5.widgets import CKEditor5Widget

from .ai_translate import translate_pt_to_en


class TranslateAdminMixin:
    """Adds a "Translate" button to the add/change form that machine-translates
    every *_pt_br field present on the form into its *_en counterpart via
    Claude. Works for any ModelAdmin that also uses modeltranslation's
    TranslationAdmin -- field pairing is done client-side by naming
    convention (*_pt_br / *_en), so no per-model wiring is needed beyond
    adding this mixin and the template.
    """

    change_form_template = "admin/core/translate_change_form.html"

    def get_urls(self):
        custom = [
            path(
                "translate-fields/",
                self.admin_site.admin_view(self.translate_fields_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_translate_fields",
            ),
        ]
        return custom + super().get_urls()

    def translate_fields_view(self, request):
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("invalid json")

        fields = payload.get("fields", {})
        html_fields = set(payload.get("html_fields", []))

        try:
            translated = {
                name: translate_pt_to_en(text, is_html=name in html_fields)
                for name, text in fields.items()
            }
        except Exception as exc:  # anthropic/network errors -> surface to the admin UI
            return JsonResponse({"error": str(exc)}, status=502)

        return JsonResponse(translated)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["ckeditor_field_names"] = self._ckeditor_field_names(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["ckeditor_field_names"] = self._ckeditor_field_names(request, None)
        return super().add_view(request, form_url, extra_context)

    def _ckeditor_field_names(self, request, object_id):
        obj = self.get_object(request, object_id) if object_id else None
        form_class = self.get_form(request, obj)
        form = form_class()
        return [
            name
            for name, field in form.fields.items()
            if isinstance(field.widget, CKEditor5Widget)
        ]
