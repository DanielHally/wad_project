from django.contrib import admin

from gsr.models import Category, Review, ReviewReply, Shop

# Register your models here.

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(Shop)
