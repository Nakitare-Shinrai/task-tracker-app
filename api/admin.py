from django.contrib import admin
from .models import Client, UserRoleType, Branch, CustomUser, Task

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email','address')

@admin.register(UserRoleType)
class UserRoleTypeAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'role')
    list_filter = ['user_type', 'role']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'client', 'phone', 'email')
    list_filter = ['client']
    search_fields = ('name', 'location','client__name')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'role','job_id', 'phone', 'email','password', 'branch', 'date_created')
    list_filter = ['role', 'branch','date_created']
    search_fields = ('user__username', 'job_id', 'phone','user__first_name','user__last_name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','user', 'description', 'status', 'assignee')
    list_filter = ['status', 'user', 'assignee', 'start','end']
    search_fields = ('title', 'description', 'user__user__username', 'assignee__user__username')