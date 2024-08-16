from django.db import models
from django.utils.text import slugify
from reader.models import UserProfile


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
        

class Forum(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    date_created = models.DateField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_forums')

    def __str__(self):
        return self.name

class Message(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='forum_messages')
    content = models.CharField(max_length=1000, null=False, blank=False)
    messenger = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_messenger')
    date_sent = models.DateField(auto_now_add=True)