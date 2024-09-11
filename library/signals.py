from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Genre
from community.models import Community


@receiver(post_save, sender=Genre)
def create_community_on_genre_save(sender, instance, created, **kwargs):
    """
    Creates an associated community when a new Genre is added to the DB.
    """
    if created:
        community = Community(
            name=f"{instance.name} Community",
            description=f'Welcome to the {instance.name} community!'
        )
        instance.community = community


@receiver(post_delete, sender=Genre)
def delete_community_post_genre_deletion(sender, instance, **kwargs):
    """
    Deletes the associated community when a genre is deleted from the DB.
    """
    instance.community.delete()
