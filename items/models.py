from django.db import models
from group_management.settings import AUTH_USER_MODEL
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Category Name", max_length=100)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_all_moderators(self):
        return self.moderator.all()
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Supplier Name", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_all_moderators(self):
        return self.moderator.all()
    
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Item Name", max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='items')
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name + ' - ' + self.category.name
    
    # overwrite the save method, each time an item is saved, the category and supplier is set to active
    def save(self, *args, **kwargs):
        self.category.is_active = True
        self.category.save()
        super(Item, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'