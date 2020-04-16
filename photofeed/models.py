from django.db import models

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    presentableFile = models.ImageField(default='download.png', blank=True)
    originalFile = models.ImageField()
    caption = models.CharField(max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(default='japneet', max_length=20, blank=True, editable=False)
    draft = models.BooleanField(default=False) 

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
