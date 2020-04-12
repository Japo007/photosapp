from django import forms
from . models import Image

class ImageForm(forms.ModelForm):    
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Image        
        fields = ('file', 'width', 'height', 'caption')
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    
    def save(self):
        image = super(ImageForm, self).save()
        return image
        