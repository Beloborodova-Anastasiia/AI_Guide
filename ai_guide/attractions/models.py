from django.db import models


class Attraction(models.Model):
    object_name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Name',
    )
    location = models.CharField(
        max_length=256,
        verbose_name='Location',
    )
    content = models.TextField(
        max_length=10000,
        verbose_name='Description',
    )

    def __str__(self):
        return self.object_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['object_name', 'location'],
                name='unique attraction'
            )
        ]
