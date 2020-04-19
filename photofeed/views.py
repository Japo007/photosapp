from . models import Photo
from .serializers import PhotoSerializer, PhotoBulkSerializer
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_bulk import BulkModelViewSet


class PhotoBulkViewSet(BulkModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoBulkSerializer
    authentication_classes = (authentication.JWTAuthentication,)

class PhotoViewSet(viewsets.ModelViewSet):    
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = (authentication.JWTAuthentication,)

class PhotoViewSetAsc(viewsets.ModelViewSet):
    queryset = Photo.objects.order_by('uploaded_at')
    serializer_class = PhotoSerializer
    authentication_classes = (authentication.JWTAuthentication,)

class PhotoViewSetDesc(viewsets.ModelViewSet):
    queryset = Photo.objects.order_by('-uploaded_at')
    serializer_class = PhotoSerializer
    authentication_classes = (authentication.JWTAuthentication,)

class PhotoViewSetMine(viewsets.ModelViewSet):    
    serializer_class = PhotoSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    def get_queryset(self):
        photos = Photo.objects.filter(user=self.request.user)
        return photos

class PhotoViewSetMyDrafts(viewsets.ModelViewSet):
    authentication_classes = (authentication.JWTAuthentication,)    
    serializer_class = PhotoSerializer
    def get_queryset(self):             
        photos = Photo.objects.filter(user=self.request.user, draft=True)
        return photos

class PhotoViewSetByUser(viewsets.ModelViewSet):
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = PhotoSerializer
    def get_queryset(self):        
        photos = Photo.objects.filter(user=self.kwargs['user_name'])
        return photos