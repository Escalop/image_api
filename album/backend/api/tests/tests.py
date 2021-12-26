from django.test import TestCase, Client
from ..models.api_page import Album, AlbumImage
from user.models import User
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from ..views.views import *
from django.contrib import auth


class ImageTest(TestCase):
    def create_topping(self, name='Whatever', tags='#whatever'):
        return AlbumImage.objects.create(name=name, tags=tags)

    def test_image_creation(self):
        t = self.create_topping()
        self.assertTrue(isinstance(t, AlbumImage))
        self.assertEqual(t.__str__(), t.title)


class Albumest(TestCase):
    def create_album(self, title='test_title', description='test_description'):
        return Album.objects.create(title=title, description=description)

    def test_album_creation(self):
        p = self.create_album()
        self.assertTrue(isinstance(p, Album))
        self.assertEqual(p.__str__(), p.title)

    def test_ingredients_have_pizza(self):
        album_image = AlbumImage.objects.create(name='Foo')
        album_1 = Album.objects.create(title='olives', description='test_olives')
        album_2 = Album.objects.create(title='nature', description='test_nature')
        album_1.image_set.add(album_image)
        album_2.image_set.add(album_image)
        self.assertEqual(album_image.image_set.count(), 2)

    def test_pizza_has_ingredients(self):
        pizza = Pizza.objects.create(name='Foo')
        olives = Topping.objects.create(title='olives', description='5 pieces')
        onion = Topping.objects.create(title='onion', description='45 g.')
        pizza.ingredients.set([olives.pk, onion.pk])
        self.assertEqual(pizza.ingredients.count(), 2)


class PizzaTestCase(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create(username='testuser', password='password')
        image = SimpleUploadedFile("pizza.jpg", content=b'', content_type='image/jpg')
        self.pizza = Pizza.objects.create(
            name='Test_pizza',
            author=self.author,
            slug='test_pizza',
            image=image
        )

    def test_valid_pizza(self):
        self.assertEqual(self.pizza.slug, 'test_pizza')
        self.assertTrue(self.pizza.image, 'pizza.jpg')


factory = APIRequestFactory

apiclient = APIClient()


class API_Test_Case(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.user = CustomUser.objects.create(username=self.username)
        self.client.force_authenticate(user=self.user)

    def test_api_topping_works(self):
        c = Client()
        response = c.get("/api/topping/")
        self.assertEqual(response.status_code, 200)

    def test_api_pizza_works(self):
        c = Client()
        response = c.get("/api/pizza/")
        self.assertEqual(response.status_code, 200)

    def test_api_users_work(self):
        c = Client()
        response = c.get("/api/users/")
        self.assertEqual(response.status_code, 200)

    def test_topping_api_post(self):
        c = Client()
        user = auth.get_user(c)
        data = {
            "title": "new",
            "description": "70 g.",
        }
        if user.is_anonymous:
            response = c.post("/api/topping/", data=data)
            self.assertEqual(response.status_code, 403)
        else:
            response = c.post("/api/topping/", data=data)
            self.assertEqual(response.status_code, 201)

    def test_pizza_api_post(self):
        c = Client()
        user = auth.get_user(c)
        data = {
            "name": "New",
            "slug": "new",
        }
        if user.is_anonymous:
            response = c.post("/api/pizza/", data=data)
            self.assertEqual(response.status_code, 403)
        else:
            response = c.post("/api/topping/", data=data)
            self.assertEqual(response.status_code, 201)

    def test_user_api_post(self):
        c = Client()
        user = auth.get_user(c)
        data = {
            "username": "new",
            "id": "7",
        }
        if user.is_anonymous:
            response = c.post("/api/users/", data=data)
            self.assertEqual(response.status_code, 403)
        else:
            response = c.post("/api/topping/", data=data)
            self.assertEqual(response.status_code, 201)

    def test_topping_single_api_get(self):
        c = Client()
        user = auth.get_user(c)
        if user.is_authenticated:
            response = c.get("/api/topping/6/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['title'], 6)

    def test_pizza_single_api_get(self):
        c = Client()
        user = auth.get_user(c)
        if user.is_authenticated:
            response = c.get("/api/pizza/3/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['name'], 3)

    def test_users_single_api_get(self):
        c = Client()
        user = auth.get_user(c)
        if user.is_authenticated:
            response = c.get("/api/users/3/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['username'], 3)



class Test_show_pizza(TestCase):
    def test_can_show_pizza_list(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_can_show_pizza(self):
        client = Client()
        response = client.get("/pizza/peperony/")

    # self.assertEqual(response.status_code, 200)

    def test_can_create_pizza(self):
        client = Client()
        user = auth.get_user(client)
        if user.is_anonymous:
            response = client.get("/addpizza/")
            self.assertEqual(response.status_code, 302)
        if user.is_authenticated:
            response = client.get("/addpizza/")
            self.assertEqual(response.status_code, 200)


class PizzaUpdateTest(TestCase):

    def setUp(self) -> None:
        self.author = CustomUser.objects.create(username='testuser', password='password')
        image = SimpleUploadedFile("pizza.jpg", content=b'', content_type='image/jpg')
        self.pizza = Pizza.objects.create(
            name='Test_pizza',
            author=self.author,
            slug='test_pizza',
            image=image
        )

    def test_valid_pizza(self):
        client = Client()
        user = auth.get_user(client)
        self.assertEqual(self.pizza.slug, 'test_pizza')
        self.assertTrue(self.pizza.image, 'pizza.jpg')
        response = client.get("/pizza/test_pizza/edit/")
        if user.is_authenticated:
            self.assertEqual(response.status_code, 302)
            self.assertTemplateUsed(response, 'pizza/recipe_edit.html')
            self.assertContains(response, 'Test_pizza')


class PizzaSearchTest(TestCase):
    def test_can_do_searching(self):
        client = Client()
        response = client.get("/search/")
        self.assertTemplateUsed(response, 'pizza/search_topping.html')
        if SearchResultView.queryset == None:
            self.assertContains(response, '')








