from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog_home')
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default="")
    likes = models.ManyToManyField(User, related_name='blog_post', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    field_of_study = models.CharField(max_length=100)
    blog_category = models.CharField(max_length=100)
    reason = models.TextField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('blog_home')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return'%s - %s' % (self.post.title, self.commenter.username)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.id})