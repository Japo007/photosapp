import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from photofeed.models import Photo
from photofeed.serializers import PhotoSerializer, PhotoBulkSerializer
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
from django.test.utils import override_settings
from django.core.files.images import get_image_dimensions

MEDIA_ROOT = tempfile.mkdtemp()

def get_temporary_image():
    image = Image.new('RGBA', size=(500, 500), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir = MEDIA_ROOT)
    image.save(file)
    file.seek(0)
    return file

def get_temporary_image_large_width():
    image = Image.new('RGBA', size=(1500, 500), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir = MEDIA_ROOT)
    image.save(file)
    file.seek(0)
    return file

def get_temporary_image_large_height():
    image = Image.new('RGBA', size=(500, 1500), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir = MEDIA_ROOT)
    image.save(file)
    file.seek(0)
    return file

def get_temporary_image_large_height_width():
    image = Image.new('RGBA', size=(1500, 1500), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir = MEDIA_ROOT)
    image.save(file)
    file.seek(0)
    return file

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PhotoViewSetTestCase(APITestCase):    

    def setUp(self):
        self.adminuser = User.objects.create_superuser('Daenerys', 'Daenerys@test.com', 'Daenerys')
        self.adminuser.save()
        response = self.client.post("/api/token/", {"username": "Daenerys", "password": "Daenerys"})
        self.assertEqual(response.status_code, 200, "The token should be successfully returned.")              
        token = response.data['access']        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_post_photo(self):      
        data = {'originalFile': get_temporary_image(), 'presentableFile': get_temporary_image(), 'caption': 'Test Post', 'user': 'Test User'}       
        response = self.client.post('/photos/', data, follow=True)       
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response.data['photo_id'])

    def test_get_photo(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Test Create')
        response = self.client.get('/photos/')                
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

    def test_update_photo_caption(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Test Update')        
        response  = self.client.patch('/photos/1/', {'caption': 'Updated_caption'})        
        self.assertEqual(200, response.status_code)        
        self.assertEqual('Updated_caption', response.data['caption'])

    def test_save_photo_draft(self):      
        data = {'originalFile': get_temporary_image(), 'presentableFile': get_temporary_image(), 'caption': 'Test Post', 'user': 'hello', 'draft': 'true'}       
        response = self.client.post('/photos/', data)
        self.assertEqual(201, response.status_code)        
        self.assertEqual(1, response.data['photo_id'])
        self.assertEqual(True, response.data['draft'])                

    def test_delete_photo(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Test Delete')        
        response  = self.client.delete('/photos/1/')        
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(Photo.objects.all()))

    def test_list_photos_all_mine_mydraft(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 1', user="John", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 2', user="John", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 3', user="Daenerys", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 4', user="Daenerys", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 5', user="Tyrion", draft=False)
        response = self.client.get('/photos/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.data))
        response = self.client.get('/photosMine/')        
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual("Daenerys", response.data[0]['user'])
        self.assertEqual("Daenerys", response.data[1]['user'])        
        response = self.client.get("/photosMyDrafts/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(True, response.data[0]['draft'])        

    def test_sort_photos_upload_date_asc(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 1', user="John", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 2', user="John", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 3', user="Daenerys", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 4', user="Daenerys", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 5', user="Tyrion", draft=False)
        response = self.client.get('/photosAsc/')        
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.data))
        upload_date = '2000-04-18T21:01:32.979110Z'        
        for entry in response.data:
            self.assertTrue(entry['uploaded_at'] > upload_date)
            upload_date = entry['uploaded_at']
    
    def test_sort_photos_upload_date_desc(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 1', user="John", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 2', user="John", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 3', user="Daenerys", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 4', user="Daenerys", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 5', user="Tyrion", draft=False)
        response = self.client.get('/photosDesc/')        
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.data))
        upload_date = '2030-04-18T21:01:32.979110Z'        
        for entry in response.data:
            self.assertTrue(entry['uploaded_at'] < upload_date)
            upload_date = entry['uploaded_at']

    def test_list_photos_filter_by_user(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 1', user="John", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 2', user="John", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 3', user="Daenerys", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 4', user="Daenerys", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 5', user="Tyrion", draft=False)        
        response = self.client.get('/photosByUser/Daenerys/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual("Daenerys", response.data[0]['user'])
        self.assertEqual("Daenerys", response.data[1]['user'])        
        response = self.client.get('/photosByUser/John/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual("John", response.data[0]['user'])
        self.assertEqual("John", response.data[1]['user'])
        response = self.client.get('/photosByUser/Tyrion/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual("Tyrion", response.data[0]['user'])

    
    def test_photo_present_dimensions(self):        
        data = {'originalFile': get_temporary_image(), 'presentableFile': get_temporary_image(), 'caption': 'Test Post', 'user': 'Test User'}       
        response = self.client.post('/photos/', data, follow=True)
        self.assertEqual(201, response.status_code)
        currPhoto = Photo.objects.all()[0]
        w, h = get_image_dimensions(currPhoto.presentableFile)
        self.assertTrue(w < 1000)
        self.assertTrue(h < 1000)
        Photo.objects.get(pk=1).delete()
        data = {'originalFile': get_temporary_image_large_width(), 'presentableFile': get_temporary_image_large_width(), 'caption': 'Test Post', 'user': 'Test User'}       
        response = self.client.post('/photos/', data, follow=True)
        self.assertEqual(201, response.status_code)
        currPhoto = Photo.objects.all()[0]
        w, h = get_image_dimensions(currPhoto.presentableFile)
        self.assertTrue(w == 1000)
        self.assertTrue(h < 1000)
        Photo.objects.all().delete()
        data = {'originalFile': get_temporary_image_large_height(), 'presentableFile': get_temporary_image_large_height(), 'caption': 'Test Post', 'user': 'Test User'}       
        response = self.client.post('/photos/', data, follow=True)
        self.assertEqual(201, response.status_code)
        currPhoto = Photo.objects.all()[0]
        w, h = get_image_dimensions(currPhoto.presentableFile)
        self.assertTrue(w < 1000)
        self.assertTrue(h == 1000)
        Photo.objects.all().delete()
        data = {'originalFile': get_temporary_image_large_height_width(), 'presentableFile': get_temporary_image_large_height_width(), 'caption': 'Test Post', 'user': 'Test User'}       
        response = self.client.post('/photos/', data, follow=True)
        self.assertEqual(201, response.status_code)
        currPhoto = Photo.objects.all()[0]
        w, h = get_image_dimensions(currPhoto.presentableFile)        
        self.assertTrue(w == 1000)
        self.assertTrue(h == 1000)

    def test_bulk_post(self):        
        data = {'originalFile': get_temporary_image(), 'presentableFile': get_temporary_image(), 'caption': 'Bulk Image 1', 'user': 'Test User', 'draft': 'true'}        
        response = self.client.post('/photosBulk/', data, follow=True)
        self.assertEqual(201, response.status_code)
        self.assertEqual('Bulk Image 1', response.data['caption'])

    def test_bulk_get(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 1', user="John", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 2', user="John", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 3', user="Daenerys", draft=False)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 4', user="Daenerys", draft=True)
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Caption 5', user="Tyrion", draft=False)                      
        response = self.client.get('/photosBulk/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.data))

    def test_bulk_update_photo_caption(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Test Update')        
        response  = self.client.patch('/photosBulk/1/', {'caption': 'Updated_caption'})        
        self.assertEqual(200, response.status_code)        
        self.assertEqual('Updated_caption', response.data['caption'])

    def test_bulk_delete_photo(self):
        Photo.objects.create(presentableFile=get_temporary_image().name, originalFile=get_temporary_image().name, caption='Test Bulk Delete')        
        response  = self.client.delete('/photosBulk/1/')        
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(Photo.objects.all()))