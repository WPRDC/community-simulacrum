from django.db import models


class Identified(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    @property
    def title(self):
        return self.name.capitalize()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Described(Identified):
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
