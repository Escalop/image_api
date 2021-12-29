import io
import json
import tempfile
from unittest import mock
from PIL import Image
from django.core.files import File
from django.urls import reverse
from rest_framework import status
from model_bakery import baker
from api.models import Album, AlbumImage
from user.models import User
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client


class API_Test_Case(APITestCase):
    def setUp(self):
        user = User.objects.create(username='lauren')
        user.set_password('secret')
        user.save()
        self.one_album = Album.objects.create(
            title='My_album',
            description='random',
            owner=user,
            is_visible=True
        )
        self.album = {
            "title": "Nature",
            "description": "Ocean",
            "is_visible": "True",
            "created": "2021-11-27T15:17:10.375877",
            "owner": user,
        }
        self.valid_album = {
            "title": "valid_title",
            "description": "valid_description"
        }

    def test_api_album_post(self):
        c = Client()
        logged_in = c.login(username='lauren', password='secret')
        response = c.post("/api/albums/", data=self.album, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_api_album_get(self):
        c = Client()
        logged_in = c.login(username='lauren', password='secret')
        response = c.get("/api/albums/", kwargs={"pk": self.one_album.id})
        self.assertEqual(response.status_code, 200)

    def test_api_album_get_list(self):
        c = Client()
        logged_in = c.login(username='lauren', password='secret')
        response = c.get("/api/albums/")
        self.assertEqual(response.status_code, 200)

    def test_api_album_update(self):
        c = Client()
        logged_in = c.login(username='lauren', password='secret')
        response = c.put(reverse('album_detail', kwargs={"pk": self.one_album.id}),
                         data=json.dumps(self.valid_album), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_api_album_delete(self):
        c = Client()
        logged_in = c.login(username='lauren', password='secret')
        response = c.delete(reverse('album_detail', kwargs={"pk": self.one_album.id}))
        self.assertEqual(response.status_code, 204)

    def tearDown(self) -> None:
        print('tearDown/n')


class API_Test_Case_Image(APITestCase):
    def setUp(self):
        user = User.objects.create(username='jennifer')
        user.set_password('secret12345')
        user.save()
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'Cat03.jpg'
        self.one_image = AlbumImage.objects.create(
            name='test',
            owner=user,
            tags='#test',
            pic=file_mock.name,
            created="2021-11-25T15:17:10.375877",
            album=baker.make(Album)
        )

        image = io.BytesIO()
        image = Image.new('RGB', (1152, 2048))
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(file)
        image.seek(0)
        image = SimpleUploadedFile("Cat03.jpg", content=b'', content_type='image/jpg')
        self.album_data = {
            "title": "Test",
            "description": "Test",
            "is_visible": "True",
            "created": "2021-11-23T15:17:10.375877",
            "owner": user,
        }

        self.image = {
            "name": "test",
            "tags": "#test",
            "pic": file,
            "created": "2021-11-25T15:17:10.375877",
            "owner": user,
            "album": self.album_data,
            }
        self.valid_image = {
            "name": "valid_name",
            "tags": "valid_tags"

        }

    '''def test_api_image_post(self):
        c = Client()
        logged_in = c.login(username='jennifer', password='secret12345')
        serializer_data = ImageSerializer(self.one_image).data
        response = c.post("/api/images/", data=self.image, format='multipart')
        serializer_data = ImageSerializer(self.one_image).data

        self.assertEqual(response.status_code, 201)
        self.assertEqual(serializer_data, response.data)
        print(response.data)'''

    def test_api_image_list_get(self):
        c = Client()
        logged_in = c.login(username='jennifer', password='secret12345')
        response = c.get("/api/images/")
        self.assertEqual(response.status_code, 200)

    def test_api_image_get(self):
        c = Client()
        logged_in = c.login(username='jennifer', password='secret12345')
        response = c.get("/api/images/", kwargs={"pk": self.one_image.id})
        self.assertEqual(response.status_code, 200)

    '''def test_api_image_update(self):
        c = Client()
        logged_in = c.login(username='jennifer', password='secret12345')
        response = c.put(reverse('image_detail', kwargs={"pk": self.one_image.id}),
                         data=json.dumps(self.valid_image), content_type='application/json')
        self.assertEqual(response.status_code, 200)'''

    def test_api_image_delete(self):
        c = Client()
        logged_in = c.login(username='jennifer', password='secret12345')
        response = c.delete(reverse('image_detail', kwargs={"pk": self.one_image.id}))
        self.assertEqual(response.status_code, 204)


class AuthenticationTestCase(APITestCase):

    def registration(self):
        data = {'username': "alina", "password": "secret123"}
        response = self.client.post("rest-auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
