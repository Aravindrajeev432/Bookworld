from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password=None):
        if not email :
            raise ValueError("User must have email")
        if not first_name :
            raise ValueError("user  must have first name")
        if not last_name :
            raise ValueError("User must have last name")
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,first_name,last_name,password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password=password,
            
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
class Account(AbstractBaseUser):
    first_name =  models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    
    email = models.EmailField(max_length=100 , unique=True)
    Phone_number = models.CharField(max_length=50,null = True, blank=True)
    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin =  models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_blocked =  models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True
