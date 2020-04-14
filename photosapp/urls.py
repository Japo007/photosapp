"""photosapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from photofeed.views import PhotoViewSet, PhotoViewSetAsc, PhotoViewSetDesc, PhotoViewSetMine, PhotoViewSetMyDrafts, PhotoViewSetByUser, PhotoViewSetAsDraft

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('photos', PhotoViewSet, basename='photos')
router.register('photosAsDraft', PhotoViewSetAsDraft, basename='photosAsDraft')
router.register('photosAsc', PhotoViewSetAsc, basename='photosAsc')
router.register('photosDesc', PhotoViewSetDesc, basename='photosDesc')
router.register('photosMine', PhotoViewSetMine, basename='photosMine')
router.register('photosMyDrafts', PhotoViewSetMyDrafts, basename='photosMyDrafts')
router.register('photosByUser/(?P<user_name>.+?)', PhotoViewSetByUser, basename='photosByUser')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^photos/',views.PhotoList.as_view()),
]

urlpatterns += router.urls

#Add Django site authentication urls (for login, logout, password management)
"""
urlpatterns += [
    path('photofeed/', include('django.contrib.auth.urls')),
    path('photofeed/profile/', views.profile, name='profile'),    
]
"""

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)