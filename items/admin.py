from django.contrib import admin
from . models import Category, Supplier, Item


class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name',]
    list_filter = ['name',]
    list_per_page = 10
    ordering = ['name', 'created_at']


class AdminSupplier(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name',]
    list_filter = ['name',]
    list_per_page = 10
    ordering = ['name', 'created_at']


class AdminItem(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name',]
    list_filter = ['name',]
    list_per_page = 10
    ordering = ['name', 'created_at']


admin.site.register(Category, AdminCategory)
admin.site.register(Supplier, AdminSupplier)
admin.site.register(Item, AdminItem)
