from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Client, UserRoleType, Branch, CustomUser, Task
from django.contrib.auth.models import User
from django.utils import timezone

class APITestSetup(APITestCase):
    def setUp(self):
        # Create a client
        self.client_obj = Client.objects.create(
            name="Test Client",
            email="client@example.com"
        )
        # Create a user role type
        self.role = UserRoleType.objects.create(
            user_type="manager",
            role="manager"
        )
        # Create a branch
        self.branch = Branch.objects.create(
            name="Main Branch",
            location="HQ",
            client=self.client_obj
        )
        # Create Django User and CustomUser for main user
        self.django_user = User.objects.create_user(username="testuser", password="pass1234")
        self.user = CustomUser.objects.create(
            user=self.django_user,
            role=self.role,
            job_id="U001",
            phone="1234567890",
            email="testuser@example.com",
            password="pass1234",
            branch=self.branch
        )
        # Create Django User and CustomUser for assignee
        self.django_assignee = User.objects.create_user(username="assignee", password="pass1234")
        self.assignee = CustomUser.objects.create(
            user=self.django_assignee,
            role=self.role,
            job_id="U002",
            phone="0987654321",
            email="assignee@example.com",
            password="pass1234",
            branch=self.branch
        )
        now = timezone.now()
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Desc",
            user=self.user,
            assignee=self.assignee,
            status="pending",
            start=now,
            end=now
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.django_user)

class ClientViewSetTests(APITestSetup):
    def test_list_clients(self):
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_client(self):
        url = reverse('client-list')
        data = {"name": "New Client", "email": "newclient@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserRoleTypeViewSetTests(APITestSetup):
    def test_list_roles(self):
        url = reverse('userroletype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_role(self):
        url = reverse('userroletype-list')
        data = {"user_type": "staff", "role": "agent"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class BranchViewSetTests(APITestSetup):
    def test_list_branches(self):
        url = reverse('branch-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_branches_by_client(self):
        url = reverse('branch-list')
        response = self.client.get(url, {'client_id': self.client_obj.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b['client'] == self.client_obj.id for b in response.data))

class UserViewSetTests(APITestSetup):
    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_users_by_role(self):
        url = reverse('user-list')
        response = self.client.get(url, {'role_id': self.role.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(u['role'] == self.role.id for u in response.data))

    def test_filter_users_by_branch(self):
        url = reverse('user-list')
        response = self.client.get(url, {'branch_id': self.branch.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(u['branch'] == self.branch.id for u in response.data))

class TaskViewSetTests(APITestSetup):
    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_user(self):
        url = reverse('task-list')
        response = self.client.get(url, {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(t['user'] == self.user.id for t in response.data))

    def test_filter_tasks_by_assignee(self):
        url = reverse('task-list')
        response = self.client.get(url, {'assignee_id': self.assignee.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(t['assignee'] == self.assignee.id for t in response.data))

    def test_filter_tasks_by_status(self):
        url = reverse('task-list')
        response = self.client.get(url, {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(t['status'] == 'pending' for t in response.data))