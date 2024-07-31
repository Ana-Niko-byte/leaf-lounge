from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile for maintaining default delivery information,
    order history, and saved books.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    default_country = CountryField(
        blank_label='Country *',
        null=True,
        blank=True
    )
    default_postcode = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    default_town_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )
    default_street_1 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    default_street_2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    default_county = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username}'

    @receiver(post_save, sender=user)
    def create_or_save_profile(sender,  instance, created, **kwargs):
        """
        Handles the creation of user profiles for new users,
        and updates for existing users.
        """
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()
