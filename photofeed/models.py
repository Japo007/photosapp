from django.db import models

class Imager(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    bio = models.CharField(max_length=180, blank=True, null=True)

    def __str__(self):
        return self.firstname

class Image(models.Model):
    file = models.ImageField()
    caption = models.CharField(max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=20, default='japneet')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
