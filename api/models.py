from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserRoleType(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('client', 'Client'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('team_lead', 'Team Leader'),
        ('agent', 'Agent'),
        ('client', 'Client'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.get_user_type_display()} - {self.get_role_display()}"

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='branches')
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.client.name}"

class CustomUser(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   role = models.ForeignKey(UserRoleType, on_delete=models.PROTECT)
   job_id = models.CharField(max_length=50, unique=True)
   phone = models.CharField(max_length=20)
   email = models.EmailField(unique=True)
   password = models.CharField(max_length=128)
   branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='users')
   date_created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return f"{self.user.get_full_name()} - {self.role.get_role_display()}"
   
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.get_status_display()} on date {self.created_at.strftime('%Y-%m-%d')}"