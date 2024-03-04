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
GROUP_TASK_URL = reverse('api:list-group-tasks')
GROUP_QUEUE_URL = reverse('api:list-group-queue')


def detail_group_url(pk):
    """Create and return a group detail URL."""
    return reverse('api:group-detail', args=[pk])

def detail_group_task_url(pk):
    """Create and return a group task detail URL."""
    return reverse('api:update-group-task', args=[pk])


def create_group_task(**params):
    """Create and return a sample Group Task."""
    return GroupTask.objects.create(**params)


def create_group_queue(**params):
    """Create and return a sample Group Queue."""
    return GroupQueue.objects.create(**params)


def create_group(**params):
    """Create and return a sample Group."""

    group = Group.objects.create(**params)
    return group


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PrivateGroupApiTests(TestCase):
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
        self.assertEqual(group.description, payload['description'])

    
    def test_group_task_creation(self):
        """Test creating a group task."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        self.assertEqual(group_queue.status, False)
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        self.assertEqual(group_task.status, False)
        self.assertEqual(group_task.comment, 'This is a test comment')

    
    def test_group_update_task(self):
        """Test updating a group task."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        payload = {'status': True, 'comment': 'This is an updated test comment'}
        res = self.client.patch(detail_group_task_url(group_task.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        group_task.refresh_from_db()
        self.assertEqual(group_task.status, payload['status'])
        self.assertEqual(group_task.comment, payload['comment'])

    
    def test_group_task_list(self):
        """Test getting group tasks."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        res = self.client.get(GROUP_TASK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = GroupTaskSerializer(group_task)
        self.assertEqual(res.data[0], serializer.data)


    def test_group_task_detail(self):
        """Test getting a single group task."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        res = self.client.get(detail_group_task_url(group_task.id))
        serializer = GroupTaskSerializer(group_task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    
    def test_update_group_task_user_status_forbidden(self):
        """Test updating a group task user status."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        # login with another user
        sample_user = create_user(
            email='another_user@gmail.com', password='test123'
        )
        self.client.force_authenticate(sample_user)
        payload = {'status': True}
        res = self.client.patch(detail_group_task_url(group_task.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_group_task_user_status_approved(self):
        """Test updating a group task user status."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        group_task = create_group_task(
            group_queue=group_queue,
            user=self.user,
            comment='This is a test comment'
        )
        payload = {'status': True}
        res = self.client.patch(detail_group_task_url(group_task.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        group_task.refresh_from_db()
        self.assertEqual(group_task.status, payload['status'])


    def test_group_queue_creation(self):
        """Test creating a group queue."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        self.assertEqual(group_queue.group, group)
        self.assertEqual(group_queue.created_by, self.user)
        self.assertEqual(group_queue.status, False)

    
    def test_group_queue_list(self):
        """Test getting group queues."""
        group = create_group(
            name='Test Group',
            description='This is a test group',
            created_by=self.user
        )
        group_queue = create_group_queue(
            group=group,
            created_by=self.user
        )
        res = self.client.get(GROUP_QUEUE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

        