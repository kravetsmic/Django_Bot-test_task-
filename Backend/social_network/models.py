from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    publication_date = models.DateTimeField(
        default=timezone.now, editable=False
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    text = models.TextField()
    views = models.ManyToManyField(
        User, related_name="viewed_posts", blank=True
    )
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True
    )

    class Meta:
        db_table = "post"
