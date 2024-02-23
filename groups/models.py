from django.db import models
from group_management.settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

    
class Group(models.Model):
    name = models.CharField("Group Name", max_length=255)
    description = models.TextField("Group Description", blank=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='groups_created')
    moderator = models.ManyToManyField(AUTH_USER_MODEL, related_name='moderators')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_all_moderators(self):
        return self.moderator.all()
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'



@receiver(post_save, sender=Group)
def check_admin(sender, instance, created, **kwargs):
    if created:
        instance.moderator.add(instance.created_by)
        instance.save()
    else:
        instance.save()


    