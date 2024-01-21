from django.db import models
from django_quill.fields import QuillField

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = QuillField()
    created_at = models.DateTimeField(auto_now_add=True)

    