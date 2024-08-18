from django.db import models
from django.shortcuts import reverse
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
    """
    A class representing a community forum.

    Fields:
    name : CharField - the forum name.
    slug : SlugField - the forum slug as name-community-id.
    date_created : DateField - the date the forum was created on.
    community: FK : Community - the forum community.
    """
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_forums')

    def __str__(self):
        """
        :returns : (str) : (forum name)
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Saves a custom url to the (self.slug) parameter as
        (forum title)-(forum community)-(forum id).

        Note : Done so for the purposes of omitting probability of url clashes
        in case forums in the same community have the same name.
        """
        try:
            if not self.slug or self.slug != slugify(self.name) + '-' + slugify(self.community) + '-' + str(self.id):
                self.slug = slugify(self.name) + '-' + slugify(self.community) + '-' + str(self.id)
            super(Forum, self).save(*args, **kwargs)
        except Forum.DoesNotExist:
            super(Forum, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        """
        :returns : the forum detail page with (self.slug) as url argument.
        """
        return reverse('forum_detail', args=[self.slug])

class Message(models.Model):
    """
    A class representing a message in a community forum.

    Fields:
    forum: FK : Forum - the forum to which the message belongs.
    content : CharField - the message content.
    messenger : FK : UserProfile - the user author of the message.
    date_sent : DateField - the date the message was sent on.
    """
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='forum_messages')
    content = models.CharField(max_length=1000, null=False, blank=False)
    messenger = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_messenger')
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :returns : (str) : (messagename)
        """
        return f"Message in '{self.forum.name}'"