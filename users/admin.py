from django.contrib import admin
from . models import CustomUser, AuditLog

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AuditLog)
