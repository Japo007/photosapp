from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from photofeed.views import PhotoViewSet, PhotoViewSetAsc, PhotoViewSetDesc, PhotoViewSetMine, PhotoViewSetMyDrafts, PhotoViewSetByUser, PhotoBulkViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

router = DefaultRouter()
router.register('photos', PhotoViewSet, basename='photos')
router.register('photosAsc', PhotoViewSetAsc, basename='photosAsc')
router.register('photosDesc', PhotoViewSetDesc, basename='photosDesc')
router.register('photosMine', PhotoViewSetMine, basename='photosMine')
router.register('photosMyDrafts', PhotoViewSetMyDrafts, basename='photosMyDrafts')
router.register('photosByUser/(?P<user_name>.+?)', PhotoViewSetByUser, basename='photosByUser')

bulkRouter = BulkRouter()
bulkRouter.register('photosBulk', PhotoBulkViewSet, basename='photosBulk')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

urlpatterns += bulkRouter.urls

#Add Django site authentication urls (for login, logout, password management)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
