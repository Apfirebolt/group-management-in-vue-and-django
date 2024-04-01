from django.db import models
from group_management.settings import AUTH_USER_MODEL
from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete
from django.dispatch import receiver
from users.models import AuditLog

    
class Group(models.Model):
    name = models.CharField("Group Name", max_length=255)
    description = models.TextField("Group Description", blank=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='groups_created')
    moderator = models.ManyToManyField(AUTH_USER_MODEL, related_name='group_moderators', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_all_moderators(self):
        return self.moderator.all()
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'



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
        return self.group.name + ' - ' + self.created_by.email


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
        return self.group_queue.group.name + ' - ' + self.user.email
        


def handle_m2m_change(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        # create a new group queue
        group_queue = GroupQueue.objects.create(group=instance, created_by=instance.created_by)
        group_queue.save()
        
        # capture all the moderators and create a group queue for each moderator
        moderators = instance.get_all_moderators()
        for moderator in moderators:
            # create a new group task for moderator and set status as 'Pending' if the task was not already created
            group_task = GroupTask.objects.create(group_queue=group_queue, user=moderator, status=False)
            group_task.save()


# audit log for group
@receiver(post_save, sender=Group)
def log_group_audit(sender, instance, **kwargs):
    if kwargs['created']:
        action = 'CREATE'
    else:
        action = 'UPDATE'
    AuditLog.objects.create(
        model_name=sender.__name__,
        object_id=instance.id,
        action=action,
        message=f'Group {instance.name} created' if action == 'CREATE' else f'Group {instance.name} updated',
        created_by=instance.created_by
    )

# audit log for group task
@receiver(post_save, sender=GroupTask)
def log_group_task_audit(sender, instance, **kwargs):
    message = ''
    if kwargs['created']:
        action = 'CREATE'
        message = f'Group Task {instance.group_queue.group.name} created by {instance.user.email}'
    else:
        action = 'UPDATE'
        if instance.status:
            action = 'APPROVED'
            message = f'Group Task {instance.group_queue.group.name} approved by {instance.user.email}'
        else:
            message = f'Group Task {instance.group_queue.group.name} rejected by {instance.user.email}'
        
    AuditLog.objects.create(
        model_name=sender.__name__,
        object_id=instance.id,
        action=action,
        message=message,
        created_by=instance.user
    )

# audit log for group delete
@receiver(pre_delete, sender=Group)
def log_group_delete_audit(sender, instance, **kwargs):
    action = 'DELETE'
    AuditLog.objects.create(
        model_name=sender.__name__,
        object_id=instance.id,
        action=action,
        message=f'Group {instance.name} deleted by {instance.created_by.email}',
        created_by=instance.created_by
    )


# Connect the signal to the m2m_changed signal of the Group.moderator field
m2m_changed.connect(handle_m2m_change, sender=Group.moderator.through)

        

    