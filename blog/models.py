from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')

class Post(models.Model):
    tags = TaggableManager()

    objects = models.Manager() # default manager, if there isn`t a manager it`s creating automatically
    published = PublishedManager() # custom manager

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=100, help_text='Enter title')
    content = models.TextField()
    #slug = models.SlugField(max_length=250,unique_for_date='publish')

    date_create = models.DateTimeField(default=timezone.now)
    date_publish = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='draft')

    class Meta:

        ordering = ['-date_publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Section(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    email = models.EmailField()
    body = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_create',)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'


