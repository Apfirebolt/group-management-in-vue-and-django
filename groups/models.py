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


class GroupQueue(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_queue')
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_queue')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Group Queue'
        verbose_name_plural = 'Group Queues'
    
    def __str__(self):
        return self.group.name + ' - ' + self.created_by.username


class GroupTask(models.Model):
    """
    Multiple tasks can be created for a group queue
    """
    group_queue = models.ForeignKey(GroupQueue, on_delete=models.CASCADE, related_name='group_task')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_task')
    status = models.BooleanField(default=False)
    comment = models.TextField("Comment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Group Task'
        verbose_name_plural = 'Group Tasks'
    
    def __str__(self):
        return self.group.name + ' - ' + self.user.username + ' - ' + self.task


    