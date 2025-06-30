from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    -AbstractUser is used to Customize and add more fields in Default Django User Model. 
    -Default Django User Model has only specific fields like id, username, first_name,last_name
    email, groups, is_active, is_staff, is_superuser,date_joined ONLY.
    -From These all fields again username and password are Required(Mandetory).
    -null=True -->  batabase can store empty value
    -blank=True --> form can pass empty value 
    -null=True --> Doesn't recommended for 'CharField and TextField'
    """ 
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
