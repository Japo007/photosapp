from .models import Photo
from rest_framework import serializers
from django.core.files.images import get_image_dimensions


class PhotoSerializer(serializers.ModelSerializer):
    file = serializers.ImageField()

    def validate_file(self, file):
        # 12MB
        MAX_FILE_SIZE = 12000000
        w, h = get_image_dimensions(file)
        print("File size and dimensions")
        print(file.size)
        print(w)
        print(h)
        if file.size > MAX_FILE_SIZE:
            print(file.size)
            raise ValidationError("File size too big!")            
        else:
            #3840 x 2160 4K
            if (w > 3840) or (h > 2160):
                raise ValidationError("File dimensions are greater than 4K!")
            else:
                print("File is smaller than max size and small dimensions")
        return file

    class Meta:
        model = Photo        
        fields = '__all__'

    
