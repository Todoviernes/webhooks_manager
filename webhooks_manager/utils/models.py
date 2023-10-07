"""Django models utilities."""

# Django
from django.db import models
from slugify import slugify


class ManagerModel(models.Model):
    """PariModel base model.
    PariModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )
    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was last modified.",
    )

    class Meta:
        """Meta option."""

        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class SlugModel(models.Model):
    """SlugModel base model.
    SlugModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + slug (SlugField): Store the slug of the object.
    """

    name = models.CharField(max_length=255)
    slug_name = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name, separator="-")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        """Meta option."""

        abstract = True
