from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging
logger = logging.getLogger(__name__)

from .models import BookLineItem


@receiver(post_save, sender=BookLineItem)
def update_post_save(sender, instance, created, **kwargs):
    """
    Updates the order total when booklineitem is updated/created.
    """
    print('signal received')
    logger.debug(f"Signal received for BookLineItem with ID: {instance.id}")
    # Signals are received but function does not appear to execute.
    instance.order.update_order_total()


@receiver(post_delete, sender=BookLineItem)
def update_post_delete(sender, instance, **kwargs):
    """
    Updates the order total when booklineitem is deleted.
    """
    instance.order.update_order_total()
