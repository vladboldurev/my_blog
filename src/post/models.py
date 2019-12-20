from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.utils import timezone


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    overview = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='covers/', null=True, blank=True)
    category = models.ManyToManyField('Category')
    featured = models.BooleanField(default=True)
    content = models.TextField()
    prev_post = models.ForeignKey('self', related_name='prev', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index')
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('post_update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'id': self.id})

    @property
    def get_comments(self):
        return self.comments.all()

    @property
    def comment_count(self):
        return self.comments.all().count()


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    post = models.ManyToManyField(Post, related_name='hash_tag')

    def __str__(self):
        return self.name
