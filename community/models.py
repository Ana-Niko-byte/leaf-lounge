from django.db import models


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

    def __str__(self):
        return f'{self.name}'
