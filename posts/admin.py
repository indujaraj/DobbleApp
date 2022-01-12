from django.contrib import admin

from posts.models import Post, Comment, ThreadModel, MessageModel


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'image')
    list_filter = ('likes', 'dislikes',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'comment']
    list_filter = ('user',)


@admin.register(ThreadModel)
class ThreadModelAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2']
    list_filter = ('user1', 'user2')


@admin.register(MessageModel)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['thread', 'user1', 'user2', 'body', ]
    list_filter = ('user1', 'user2')
