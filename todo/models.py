from django.db import models
from django.contrib.auth import get_user_model


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    # User who posted todo
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title
