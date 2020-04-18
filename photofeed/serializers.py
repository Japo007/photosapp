from .models import Photo
from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from easy_thumbnails.files import get_thumbnailer



class PhotoSerializer(serializers.ModelSerializer):
    originalFile = serializers.ImageField()
    #presentableFile = serializers.ImageField()
    user = serializers.CharField()
    
    def validate(self, data):
        print("In validate")
        file = data['originalFile']
        w, h = get_image_dimensions(file)
        resized_image = None        
        if (w > 1000) and (h > 1000):
            thumbnail_options = {
                'crop': 'smart',
                'upscale': True,
                'size': (1000, 1000)
            }
            resized_image = get_thumbnailer(data['originalFile'],'presentableFile').get_thumbnail(thumbnail_options)
            data['presentableFile'] = resized_image.url.split("/")[2]
        elif (w < 1000) and (h > 1000):
            thumbnail_options = {
                'crop': 'smart',
                'upscale': True,
                'size': (1000, 0)
            }
            resized_image = get_thumbnailer(data['originalFile'],'presentableFile').get_thumbnail(thumbnail_options)
            data['presentableFile'] = resized_image.url.split("/")[2]
        elif (w > 1000) and (h < 1000):
            thumbnail_options = {
                'crop': 'smart',
                'upscale': True,
                'size': (0, 1000)
            }
            resized_image = get_thumbnailer(data['originalFile'],'presentableFile').get_thumbnail(thumbnail_options)
            data['presentableFile'] = resized_image.url.split("/")[2]                
        else:
            data['presentableFile'] = data['originalFile']        
        currUser = None        
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            currUser = request.user
        data['user'] = currUser       
        return data


    class Meta:
        model = Photo              
        fields = '__all__'