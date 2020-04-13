from .models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        #fields = ['file', 'originalFile', 'caption', 'uploaded_at', 'user', 'draft']
        fields = '__all__'
