import json

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
    misataken_names = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    # def set_misataken_name(self, name):
    #     if self.misataken_names:
    #         misataken_names = self.misataken_names
    #         misataken_names.append(name)
    #     else:
    #         self.misataken_name = json.dumps(name)
    #     self.misataken_name = json.dumps(misataken_names)

    def get_misataken_name(self):
        return json.loads(self.misataken_name)

    def __str__(self):
        return self.object_name
