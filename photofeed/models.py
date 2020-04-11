from django.db import models

class User(models.Model):
    firstname = models.charField(max_length=10)
    lastname = models.charField(max_length=10)
    bio = models.charField(max_length=180, blank=True, null=True)

    def __str__(self):
        return self.firstname

class Image(models.Model):
    file = models.ImageField()
    caption = models.charField(max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)
