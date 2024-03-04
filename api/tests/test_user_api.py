"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import CustomUserSerializer

CREATE_USER_URL = reverse('api:signup')
TOKEN_URL = reverse('api:signin')
USERS_URL = reverse('api:list-users')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def detail_user_url(pk):
    """Create and return a group detail URL."""
    return reverse('api:user-detail', args=[pk])


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'username': 'Test Name',
            'role': 'Moderator'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertTrue(user.role, payload['role'])
        self.assertNotIn('password', res.data)

    
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'username': 'Test Username',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'username': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
        self.assertIn('username', res.data)
        self.assertIn('email', res.data)
        self.assertIn('id', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': '', 'username': 'My User'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(detail_user_url(1))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateGroupApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123', username='Test Name', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)


    def test_retrieve_user_success(self):
        """Test retrieving user is successful."""
        res = self.client.get(detail_user_url(self.user.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check if user key is there in the response
        self.assertIn('username', res.data)


    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user."""
        payload = {'username': 'newname', 'password': 'newpassword123'}
        res = self.client.patch(detail_user_url(self.user.id), payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    


    
