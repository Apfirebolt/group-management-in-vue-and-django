"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import CategorySerializer
from items.models import Category


CREATE_CATEGORY_URL = reverse('api:create-category')
LIST_CATEGORIES_URL = reverse('api:list-categories')


def detail_category_url(pk):
    """Create and return a Category detail URL."""
    return reverse('api:category-detail', args=[pk])


def create_category(**params):
    """Create and return a sample Category."""

    category = Category.objects.create(**params)
    return category


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PrivateCategoryApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

   
    def test_create_category(self):
        """Test creating category with valid payload is successful."""
        payload = {'name': 'Test Category', 'created_by': self.user.id}
        res = self.client.post(CREATE_CATEGORY_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    
    def test_get_categories(self):
        """Test getting categoriess."""
        res = self.client.get(LIST_CATEGORIES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_delete_category_success(self):
        """Test deleting a question is successful."""
        category = create_category(
            name='Test Category',
            created_by=self.user
        )
        res = self.client.delete(detail_category_url(category.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        category_exists = Category.objects.filter(
            name=category.name
        ).exists()
        self.assertFalse(category_exists)

    
    def test_update_category(self):
        """Test updating a category with valid payload is successful."""
        category = create_category(
            name='Test Category',
            created_by=self.user
        )
        payload = {'name': 'Updated Category'}
        res = self.client.patch(detail_category_url(category.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])


   
