from .models import Photo
from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from rest_framework.exceptions import ValidationError
from easy_thumbnails.files import get_thumbnailer



class PhotoSerializer(serializers.ModelSerializer):
    file = serializers.ImageField()
    user = serializers.CharField()
    
    def validate(self, data):
        MAX_FILE_SIZE = 12000000
        file = data['file']
        w, h = get_image_dimensions(file)
        if file.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")
        else:
            #3840 x 2160 4K
            if (w > 1000) and (h > 1000):
                thumbnail_options = {
                    'crop': 'smart',
                    'upscale': True,
                    'size': (600, 600)
                }
            else if 
                    resized_image = get_thumbnailer(yourmodel.image).get_thumbnail(thumbnail_options)
                #raise ValidationError("File dimensions are greater than 4K!")               
        currUser = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            currUser = request.user
        print('Current user ', data['user'])
        print('Request user ', currUser)
        data['user'] = currUser
        
        return data


    class Meta:
        model = Photo
        #exclude = ['user']       
        fields = '__all__'

    
"""
    def validate_file(self, file):
        # 12MB
        MAX_FILE_SIZE = 12000000
        w, h = get_image_dimensions(file)
        if file.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")            
        else:
            #3840 x 2160 4K
            if (w > 3840) or (h > 2160):
                raise ValidationError("File dimensions are greater than 4K!")            
        return file"""