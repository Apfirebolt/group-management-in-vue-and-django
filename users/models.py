from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from group_management.settings import AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, max_length=255)
    username = models.CharField("User Name", unique=True, max_length=255, blank=True, null=True)
    role = models.CharField("Role", max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Super User', default=False)
    profile_image = models.ImageField("Profile Image", upload_to='profile_images/', blank=True, null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        '''Doc string for meta'''
        verbose_name_plural = "User"


class AuditLog(models.Model):
    model_name = models.CharField(max_length=255)  # Model being audited
    object_id = models.PositiveIntegerField()  # ID of the audited object
    action = models.CharField(max_length=50, choices=(  # Action performed
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ))
    change_data = models.JSONField(blank=True, null=True)  # Detailed changes (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of audit entry
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)  # User who made the change (optional)

    def __str__(self):
        return f"{self.model_name} {self.action} by {self.created_by.email}"