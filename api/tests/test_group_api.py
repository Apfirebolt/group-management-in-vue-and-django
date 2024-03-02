"""
Tests for question APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from groups.models import (
    Group,
    GroupQueue,
    GroupTask
)

from api.serializers import (
    GroupSerializer,
    GroupQueueSerializer,
    GroupTaskSerializer
)

CREATE_GROUP_URL = reverse('api:create-group')
GROUP_URL = reverse('api:list-groups')


def detail_group_url(pk):
    """Create and return a quiz detail URL."""
    return reverse('api:group-detail', args=[pk])


def create_group(**params):
    """Create and return a sample Group."""

    group = Group.objects.create(**params)
    return group


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)



class PrivatequestionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)


    def test_create_group_success(self):
        """Test creating a group is successful."""
        
        payload = {'name': 'Test Group', 'description': 'This is a test group', 'created_by': self.user.id}
        res = self.client.post(CREATE_GROUP_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Test signal on Group Queue creation
        # group_queue = GroupQueue.objects.get(group=res.data['name'])
        # print('Group queue:', group_queue)


    def test_get_groups(self):
        """Test getting groups."""
        res = self.client.get(GROUP_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

    
    def test_delete_group_success(self):
        """Test deleting a group is successful."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        res = self.client.delete(detail_group_url(group.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        group_exists = Group.objects.filter(
            name=group.name
        ).exists()
        self.assertFalse(group_exists)


    def test_get_single_group(self):
        """Test getting a single group."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        res = self.client.get(detail_group_url(group.id))
        serializer = GroupSerializer(group)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_update_group(self):
        """Test updating a group."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        sample_user = create_user(
            email='neo_user@example.com', password='test123'
        )

        payload = {'name': 'Updated Group', 'description': 'This is an updated test group', 'created_by': sample_user.id, 'moderator': [sample_user.id]}

        res = self.client.patch(detail_group_url(group.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        group.refresh_from_db()
        self.assertEqual(group.name, payload['name'])
        
        # check if moderator was updated
        self.assertEqual(group.moderator.first().id, sample_user.id)
        self.assertEqual(group.description, payload['description'])


        
        

        