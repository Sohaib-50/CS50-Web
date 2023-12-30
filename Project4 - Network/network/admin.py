from django.contrib import admin
from .models import User, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created")

# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
