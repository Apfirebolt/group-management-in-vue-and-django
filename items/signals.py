# from .models import Supplier
# from django.dispatch import receiver
# from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
# from .models import Supplier


# @receiver(post_save, sender=Supplier)
# def send_notification(sender, instance, created, **kwargs):
#     print('Inside signal')
#     if created:
#         print('Supplier created', instance.name)


# @receiver(pre_save, sender=Supplier)
# def send_notification(sender, instance, **kwargs):
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