from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .custom_manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    #Persional Information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        unique=True, 
        error_messages= {
            'unique': "This email is already in use.",
            'blank': "Please provide an email address.",
        })
    username = models.CharField(
        max_length= 100,
        blank= True,
        unique= True,
        error_messages= {
            'unique': "This username is already in use.",
        })
    profile_image = models.ImageField(upload_to= 'profile/', default= 'profile/profile_avatar.jpg')
    cover_image = models.ImageField(upload_to= 'cover/', blank= True)
    bio = models.CharField(max_length= 120, blank= True)
    about = models.TextField(blank= True)
    followers = models.IntegerField(default= 0, blank= True)
    following = models.IntegerField(default= 0, blank= True)
    total_post = models.IntegerField(default= 0, blank= True)

    #adittional info
    joining_date = models.DateTimeField(auto_now_add= True)
    last_update = models.DateTimeField(auto_now= True)
    last_login = models.DateTimeField(null=True, blank=True)

    #permission
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'