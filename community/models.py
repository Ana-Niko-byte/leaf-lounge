from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
