from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            "email": "test@example.com",
            "password": "testpassword",
            "name": "testuser",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""

        payload = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "name": "testuser"
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test the password must be more than 8 characters"""

        payload = {
            "email": "test@example.com",
            "password": "te",
            "name": "testuser"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created forn the user"""

        payload ={
            "email": "test@example.com",
            "password": "testpassword",
            "name": "testuser"
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token', res.data) 
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""

        create_user(email="test@example.com",password="testpassword")
        payload ={
            "email": "test@example.com",
            "password": "wrongpass",
            "name": "testuser"
        }
        res=self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is created id user does't exist"""

        payload ={
            "email": "test@example.com",
            "password": "testpassword",
            "name": "testuser"
        }

        res=self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required """

        res = self.client.post(TOKEN_URL, { "email":"one","password":""})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_reterive_user_unauthorized(self):
        """Test that authentication is required for users"""

        res=self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email = 'user@example.com',
            password = 'testpasword',
            name = 'name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_reterive_profile_success(self):
        """Test reteriving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Tests that post request is not allowed on the me url"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""

        payload = {
            'name':'newname',
            'password':'newpassword'
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    

    






