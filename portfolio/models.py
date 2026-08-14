from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    screenshot = models.ImageField(upload_to="portfolio/")
    link = models.URLField()
    is_visible = models.BooleanField(
        default=True,
        help_text="Uncheck to keep a placeholder/WIP entry hidden from the live site.",
    )

    def __str__(self):
        return self.title
