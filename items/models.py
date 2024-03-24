from django.db import models
from group_management.settings import AUTH_USER_MODEL
import uuid
from simple_history.models import HistoricalRecords


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Category Name", max_length=100)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
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
    json_data = models.JSONField("Supplier Data", default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.cached_name = self.name

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        
        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))
        
        return instance

    def save(self, *args, **kwargs):

        # check if a new db row is being added
        # When this happens the `_loaded_values` attribute will not be available
        if not self._state.adding:

            # check if field_1 is being updated
            if self._loaded_values['name'] != self.name:
                # do something
                print('Name was changed', self._loaded_values['name'], self.name)

        super().save(*args, **kwargs)
        
    
    
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