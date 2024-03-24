from .models import Supplier
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from .models import Supplier
import logging
from . handlers import handle_supplier_creation

supplier_created = Signal()

supplier_created.connect(handle_supplier_creation, sender=Supplier)


@receiver(pre_save, sender=Supplier)
def store_original_name(sender, instance, **kwargs):
    """
    Store the original name of the supplier before saving.
    """
    instance._original_name = getattr(instance, 'name', None)  # Handle potential new objects
    print('Inside pre save', instance._original_name)

@receiver(post_save, sender=Supplier)
def log_name_change(sender, instance, created, **kwargs):
    """
    Log the change in a Log model if the name has changed.
    """
    print('Inside post save', instance.name, instance._original_name)
    if not created and hasattr(instance, '_original_name') and instance.name != instance._original_name:
        # Name has changed for an existing object
        old_name = instance._original_name
        new_name = instance.name
        log_message = f"Supplier name changed from '{old_name}' to '{new_name}'"
        print(log_message)
        del instance._original_name  # Cleanup after logging

# Connect the signals to the Supplier model
pre_save.connect(store_original_name, sender=Supplier)
post_save.connect(log_name_change, sender=Supplier)

# @receiver(post_save, sender=Supplier)
# def send_notification(sender, instance, created, update_fields=None, **kwargs):
#     print('Inside signal', instance.name, created, kwargs)
#     if created:
#         print('Supplier created', instance.name)
#         instance._change_reason = "Updated name for clarity"
#         logger = logging.getLogger('items')
#         logger.info(f"Updating {Supplier}: {instance.id} (Before)")
#     else:
#         print('Supplier updated', instance.name, instance)
#         logger = logging.getLogger('items')
#         logger.info(f"Updating {Supplier}: {instance.id} (After)")


# @receiver(pre_save, sender=Supplier)
# def send_notification(sender, instance, **kwargs):
#     instance._change_reason = "Changed for some reason"
#     print('Supplier is about to be saved', instance.name)

# @receiver(post_save, sender=Supplier)
# def send_notification_post_save(sender, instance, created, **kwargs):
#     print('Inside post_save signal')
#     if created:
#         print('Supplier created', instance.name)

# @receiver(pre_save, sender=Supplier)
# def send_notification_pre_save(sender, instance, **kwargs):
#     print('Supplier is about to be saved', instance.name)

# @receiver(post_delete, sender=Supplier)
# def send_notification_post_delete(sender, instance, **kwargs):
#     print('Supplier deleted', instance.name)

# @receiver(pre_delete, sender=Supplier)
# def send_notification_pre_delete(sender, instance, **kwargs):
#     print('Supplier is about to be deleted', instance.name)

# @receiver(post_delete, sender=Supplier)
# def send_notification(sender, instance, **kwargs):
#     print('Supplier deleted', instance.name)


# @receiver(pre_delete, sender=Supplier)
# def send_notification(sender, instance, **kwargs):
#     print('Supplier is about to be deleted', instance.name)