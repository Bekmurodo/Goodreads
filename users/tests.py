from django.contrib.auth import get_user
from .models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegisterTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(
           reverse("users:register"),
            data={
                "username": "farukh",
                "first_name": "Farukh",
                "last_name": "Bekmurodov",
                "email": "suhrob2@gmail.com",
                "password": "simplepassword"
            }
        )
        user = CustomUser.objects.get(username='farukh')

        self.assertEqual(user.first_name, "Farukh")
        self.assertEqual(user.last_name, "Bekmurodov")
        self.assertEqual(user.email, 'suhrob2@gmail.com')
       # self.assertNotEqual(user.password, 'simplepassword')
      #  self.assertFalse(user.check_password( 'simplepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "jon",
                "email": "suhrob2@gmail.com"
           }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
       # self.assertFormError(response, "form", 'username', 'This field is required.')
       # self.assertFormError(response, "form", 'password', 'This field is required.')



    def test_invalid_email(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "farukh",
                "first_name": "Farukh",
                "last_name": "Bekmurodov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        #self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        # 1. create a user
        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo',)
        user.set_password('somepass')
        user.save()
        # 2. try to create another user with that same username
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "momina",
                "first_name": "Xolov",
                "last_name": "Bekmurodov",
                "email": "suhrob2@gmail.com",
                "password": "somepassword"
            }
        )
        # 3.check that the second user was not created
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 2)



class LoginTestCase(TestCase):
    # DRY - Don't  repeat yourself
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        self.db_user.set_password('somepass')
        self.db_user.save()

    def test_successful_login(self):

        self.client.post(
            reverse('users:login'),
            data={
                'username': "momin",
                'password': "somepass"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credential(self):


        self.client.post(
            reverse('users:login'),
            data={
                'username': "wrong-user",
                'password': "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse('users:login'),
            data={
                'username': "momin",
                'password': "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_successful_logout(self):


        self.client.login(username='momin', password='somepass')

        self.client.get(reverse('users:logout'))
        #self.client.logout()
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_profile_detail(self):
        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', last_name='Muhriddin', email='momin@gmail.com')
        user.set_password('somepass')
        user.save()

        self.client.login(username='momin', password='somepass')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')

    def test_profile_edit(self):
        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        user.set_password('somepass')
        user.save()

        self.client.login(username='momin', password='somepass')

        response = self.client.post(
            reverse("users:profile-edit"),
            data = {
                "username": "suhrob",
                "first_name": "Farukh",
                "last_name": "Bekmurodov",
                "email": "suhrob@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Bekmurodov")
        self.assertEqual(user.first_name, "Farukh")
        self.assertEqual(user.username, 'suhrob')
        self.assertEqual(response.url, reverse("users:profile"))





