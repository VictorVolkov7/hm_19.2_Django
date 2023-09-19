from django.contrib import admin

from catalog.models import Product, Category, Contacts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'telegram', 'vk')
