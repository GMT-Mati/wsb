from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_content = models.ForeignKey(Content, on_delete=models.CASCADE)


# Create your models here.
