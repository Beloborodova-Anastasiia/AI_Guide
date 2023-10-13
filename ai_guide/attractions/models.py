from django.db import models


class Attraction(models.Model):
    object_name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Name',
        unique=True
    )
    location = models.CharField(
        max_length=256,
        verbose_name='Location',
    )
    content = models.TextField(
        max_length=1000,
        verbose_name='Description',
    )
    audio = models.FileField(
        upload_to='audio/',
        blank=True
    )

    def __str__(self):
        return self.object_name


class MisspelledNames(models.Model):
    misspelled_name = models.CharField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name='Misspelled name',
    )
    attraction = models.ForeignKey(
        Attraction,
        on_delete=models.CASCADE,
        related_name='attraction',
        verbose_name='Attraction',
    )

    def __str__(self):
        return self.misspelled_name
