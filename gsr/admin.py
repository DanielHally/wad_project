from django.contrib import admin

from gsr.models import Category, OwnerGroupRequest, Review, ReviewReply, Shop

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_approved',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(OwnerGroupRequest)
admin.site.register(Shop, ShopAdmin)
