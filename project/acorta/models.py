from django.db import models

# Create your models here.
class ShrinkedURL(models.Model):
    resource = models.URLField()
    mirror = models.URLField()
