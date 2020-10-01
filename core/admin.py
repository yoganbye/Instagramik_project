from django.contrib import admin
from .models import Profile, Comment, Post#(.) - означает что импортируем из данного каталога
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from datetime import timedelta
from django.utils import timezone

# admin.site.register(Profile)
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    # extra = 1

# class PostInline(admin.StackedInline):
#     model = Post
#     extra = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileInline]


def delete_very_old_posts(modeladmin, request, queryset):
    queryset.filter(date_pub__lte=timezone.now() - timedelta(weeks=2)).delete()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User information', {'fields': ['author']}),
        ('Post content', {'fields': ['description', 'image']}),
        ('Other information', {'fields': ['get_likes', 'date_pub']})
    ]
    # fields = ['author', 'description', 'image', 'get_likes']
    readonly_fields = ['get_likes', 'date_pub']
    list_diplay = ('author', 'date_pub', 'get_likes')
    list_filter = ('date_pub',)
    search_fields = ['description', 'author__username']
    actions = [delete_very_old_posts]

# admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# Register your models here.
