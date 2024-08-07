from django.db import models
from django.utils.text import slugify


class Community(models.Model):
    """
    A class representing a Community. 

    Fields:
    name - the name of the community.
    description - the community intro/description.

    Methods: 
    def __str__() : Returns : (str) : (community name).
    """
    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(blank=True, null=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        try:
            if not self.slug or self.slug != slugify(Community.objects.get(id=self.id).name + '-' + str(self.id)):
                self.slug = slugify(Community.objects.get(id=self.id).name + '-' + str(self.id))
            super(Community, self).save(*args, **kwargs)
        except Community.DoesNotExist:
            super(Community, self).save(*args, **kwargs)
        
