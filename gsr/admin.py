from django.contrib import admin

from gsr.models import Category, OwnerGroupRequest, Review, ReviewReply, Shop

# Register your models here.

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(OwnerGroupRequest)

class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Shop,ShopAdmin)
