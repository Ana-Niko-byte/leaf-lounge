from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_save_profile(sender,  instance, created, **kwargs):
    """
    Handles the creation of user profiles for new users,
    and updates for existing users.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()