from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Brief professional summary shown before the timeline starts. Single row, edited in admin."""

    summary = models.TextField()
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)

    def __str__(self):
        return "Profile summary"


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    redact_company_name = models.BooleanField(
        default=False,
        help_text="If checked, the public site shows company_description instead of company_name.",
    )
    company_description = models.TextField(
        blank=True,
        help_text=(
            "Short description of the company. Shown below the company name; also used as the "
            "public fallback text in place of the name when redacted."
        ),
    )
    company_website = models.URLField(
        blank=True,
        help_text="Company website. Only shown/linked when the name isn't redacted.",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for a current role.")
    description = models.TextField(
        blank=True,
        help_text="Free text: bullet points, achievements, figures, skills used.",
    )
    background_image = models.ImageField(upload_to="timeline/experience/")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Language(models.Model):
    class Proficiency(models.TextChoices):
        A1 = "a1", _("Beginner (A1)")
        A2 = "a2", _("Elementary (A2)")
        B1 = "b1", _("Intermediate (B1)")
        B2 = "b2", _("Upper Intermediate (B2)")
        C1 = "c1", _("Advanced (C1)")
        C2 = "c2", _("Proficient (C2)")
        NATIVE = "native", _("Native")

    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=10, choices=Proficiency.choices)

    class Meta:
        ordering = ["-proficiency"]

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"


class Evidence(models.Model):
    class EvidenceType(models.TextChoices):
        IMAGE = "image", "Image"
        LINK = "link", "Link"
        DOCUMENT = "document", "Document"

    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="evidence")
    evidence_type = models.CharField(max_length=10, choices=EvidenceType.choices)
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="timeline/evidence/", blank=True, null=True)
    link = models.URLField(blank=True)
    document = models.FileField(upload_to="timeline/evidence/documents/", blank=True, null=True)

    def __str__(self):
        return self.caption or f"Evidence for {self.experience}"
