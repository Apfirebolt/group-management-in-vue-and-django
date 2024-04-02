from django.contrib import admin
from . models import Group, GroupQueue, GroupTask


admin.site.register(Group)
admin.site.register(GroupQueue)
admin.site.register(GroupTask)
