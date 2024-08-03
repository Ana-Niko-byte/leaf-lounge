from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Genre
from community.models import Community


@receiver(post_save, sender=Genre)
def create_community_on_genre_save(sender, instance, created, **kwargs):
    if created:
        community = Community.objects.create(
            name=f'{instance.name} Community',
            description=f'Welcome to the {instance.name} community!',
        )
        instance.community = community
        instance.save()

@receiver(post_delete, sender=Genre)
def delete_community_post_genre_deletion(sender, instance, **kwargs):
    """
    Deletes the relevant community instance when a genre is deleted from the DB.
    """
    instance.community.delete()
