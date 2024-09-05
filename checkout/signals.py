from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import BookLineItem


@receiver(post_save, sender=BookLineItem)
def update_post_save(sender, instance, created, **kwargs):
    """
    Updates the order total when a booklineitem is updated/created.
    """
    instance.order.update_order_total()


@receiver(post_delete, sender=BookLineItem)
def update_post_delete(sender, instance, **kwargs):
    """
    Updates the order total when a booklineitem is deleted.
    """
    instance.order.update_order_total()
