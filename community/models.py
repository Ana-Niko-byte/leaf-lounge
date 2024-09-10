from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from reader.models import UserProfile


class Community(models.Model):
    """
    Represents a genre community where users can access forums, chats and
    messages. Users are granted access to the community matching the book
    genre after making purchasing a book in that genre.

    Fields:
    name : CharField - the name of the community.
    description : TextField - the community intro/description.
    slug : SlugField - the community slug.
    image : ImageField - the community header image.

    Methods:
    def __str__() -> str : Returns a string indicating the community name,
    in the format: '(community name)'.
    def save() : Saves the model instance and creates a unique slug for each
    community in the format:
    (community name)-(community id).
    """
    name = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        blank=True,
        null=False
    )
    image = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        """
        :returns -> str : (community name)
        """
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """
        Saves the model instance and creates a unique slug for each community
        in the format:
        (community name)-(community id).
        """
        try:
            super(Community, self).save(*args, **kwargs)
            if not self.slug or self.slug != slugify(
                Community.objects.get(id=self.id).name + '-' + str(self.id)
            ):
                self.slug = slugify(
                    Community.objects.get(id=self.id).name + '-' + str(self.id)
                )
            super(Community, self).save(*args, **kwargs)
        except Community.DoesNotExist:
            super(Community, self).save(*args, **kwargs)


class Forum(models.Model):
    """
    Represents a community forum. Each community can have multiple forums.
    All users inside the community have full access to forums in the
    community, and users may create new forums inside the community for
    chats and networking.

    Fields:
    name : CharField - the forum name.
    slug : SlugField - the forum slug as name-community-id.
    date_created : DateField - the date the forum was created on.
    community : FK : Community - the forum community.

    Methods:
    def __str__() -> str : Returns a string indicating the forum name,
    in the format: '(forum name)'.

    def save() : Saves the model instance. Saves a unique slug to the
    (self.slug) parameter in the format:
    (forum title)-(forum community)-(forum id).
    """
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        null=True
    )
    date_created = models.DateField(
        auto_now_add=True
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='community_forums'
    )

    def __str__(self):
        """
        :returns -> str : (forum name)
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Saves the model instance. Saves a unique slug to the
        (self.slug) parameter in the format:
        (forum title)-(forum community)-(forum id).

        Note : This slug's complexity is done for the purposes of omitting
        probability of url clashes for forums in the same communities with
        the same name.
        """
        try:
            super(Forum, self).save(*args, **kwargs)
            if not self.slug or self.slug != slugify(
                self.name
            ) + '-' + slugify(
                self.community
            ) + '-' + slugify(self.id):
                self.slug = slugify(
                    self.name
                ) + '-' + slugify(
                    self.community
                ) + '-' + slugify(self.id)
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
    Represents a message within a community forum. Messages can be
    viewed by all members of the forum, but can only be deleted by
    the user who sent the message.

    Fields:
    forum : FK : Forum - The forum to which the message belongs.
    content : CharField - The message content.
    messenger : FK : UserProfile - The user author of the message.
    date_sent : DateField - The date the message was sent on.

    Methods:
    def __str__() -> str : Returns a string indicating the a new message
    in a particular forum, in the format: "Message in '(forum name)'".
    """
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name='forum_messages'
    )
    content = models.CharField(
        max_length=1000,
        null=False,
        blank=False
    )
    messenger = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='user_messenger'
    )
    date_sent = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        :returns -> (str) : (messagename)
        """
        return f"Message in '{self.forum.name}'"
