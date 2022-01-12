from django.db import models

from socialproject.common.abstract_models import AbstractClass
from social.models import Profile


class Post(AbstractClass):
    content = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(Profile, blank=True, related_name='dislikes')

    class Meta:
        ordering = ['-created']

    def __str(self):
        return self.content[:50]


class Comment(AbstractClass):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)

    def __str__(self):
        return self.post.content[:50]


class ThreadModel(AbstractClass):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='threaduser')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='threadreceiver')

    def __str__(self):
        return self.user2.user.first_name


class MessageModel(AbstractClass):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_user')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver_user')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='message_images', blank=True, null=True)

    def __str__(self):
        return self.user1.user.first_name
