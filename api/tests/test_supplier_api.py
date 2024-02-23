"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import SupplierSerializer
from items.models import Supplier


CREATE_SUPPLIER_URL = reverse('api:create-supplier')
LIST_SUPPLIERS_URL = reverse('api:list-suppliers')


class PublicSupplierApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

   
    def test_create_supplier(self):
        """Test creating supplier with valid payload is successful."""
        payload = {'name': 'Test Supplier'}
        res = self.client.post(CREATE_SUPPLIER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    
    def test_get_suppliers(self):
        """Test getting suppliers."""
        res = self.client.get(LIST_SUPPLIERS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    


    


    
