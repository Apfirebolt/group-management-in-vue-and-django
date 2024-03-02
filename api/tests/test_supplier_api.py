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


def detail_supplier_url(pk):
    """Create and return a Supplier detail URL."""
    return reverse('api:supplier-detail', args=[pk])


def create_supplier(**params):
    """Create and return a sample Supplier."""

    supplier = Supplier.objects.create(**params)
    return supplier


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


    def test_delete_supplier_success(self):
        """Test deleting a question is successful."""
        supplier = create_supplier(
            name='Test Supplier',
        )
        res = self.client.delete(detail_supplier_url(supplier.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        supplier_exists = Supplier.objects.filter(
            name=supplier.name
        ).exists()
        self.assertFalse(supplier_exists)

    def test_update_supplier(self):
        """Test updating a supplier."""
        supplier = create_supplier(
            name='Test Supplier',
        )
        payload = {'name': 'Updated Supplier'}
        res = self.client.patch(detail_supplier_url(supplier.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        supplier.refresh_from_db()
        self.assertEqual(supplier.name, payload['name'])
    
    def test_update_supplier_not_found(self):
        """Test updating a supplier that does not exist."""
        payload = {'name': 'Updated Supplier'}
        res = self.client.patch(detail_supplier_url(1), payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_single_supplier(self):
        """Test getting a single supplier."""
        supplier = create_supplier(
            name='Test Supplier',
        )
        res = self.client.get(detail_supplier_url(supplier.id))
        serializer = SupplierSerializer(res.data)
        data = serializer.data
        self.assertTrue('name' in data)
        self.assertTrue('id' in data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], supplier.name)
