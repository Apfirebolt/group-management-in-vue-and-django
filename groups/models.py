from django.db import models
from group_management.settings import AUTH_USER_MODEL
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from users.models import CustomUser

    
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
        # Check if the user is the admin
        if instance.created_by.is_superuser:
            # create a new group task for admin and set status as 'Approved'
            group_task = GroupTask.objects.create(group_queue=group_queue, user=instance.created_by, status=True)
            group_task.save()
        
        # capture all the moderators and create a group queue for each moderator
        moderators = instance.get_all_moderators()
        for moderator in moderators:
            # create a new group task for moderator and set status as 'Pending' if the task was not already created
            group_task = GroupTask.objects.create(group_queue=group_queue, user=moderator, status=False)
            group_task.save()

        # At least one admin needs to approve creation of the group, select all admin users and for each admin user create a group task
        # with status as 'Pending'
        admin_users = CustomUser.objects.filter(is_superuser=True)
        for admin_user in admin_users:
            if admin_user == instance.created_by:
                continue
            group_task = GroupTask.objects.create(group_queue=group_queue, user=admin_user, status=False)
            group_task.save()
    

# Connect the signal to the m2m_changed signal of the Group.moderator field
m2m_changed.connect(handle_m2m_change, sender=Group.moderator.through)

        

    