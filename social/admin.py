from django.contrib import admin

from .models import User, Profile, Relationship


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
    search_fields = ('first_name', 'username', 'email')
    list_filter = ('first_name', 'email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'gender', 'image']

    list_filter = ('user',)


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
    list_filter = ('sender', 'receiver', 'status')
    search_fields = ('status',)