from django.contrib import admin
from .models import Image, Comment
# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [ 'slug', 'image', 'created']
    list_filter  = ['created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    list_filter  = ['created']
