from django.contrib import admin
from . models import User
from . models import Image

admin.site.register(User)
admin.site.register(Image)
