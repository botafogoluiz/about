from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=300, blank=True)
    # Plain TextField, not a custom CKEditor field class — django-modeltranslation
    # can only clone plain field types. The WYSIWYG editor is attached as a
    # widget in admin.py instead (formfield_overrides).
    body = models.TextField()
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title)
        if self.status == self.Status.PUBLISHED and self.published_date is None:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
