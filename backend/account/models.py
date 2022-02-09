from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, nickname, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not name:
            raise ValueError('must have user name')
        user= self.model(
            email= self.normalize_email(email),
            nickname= nickname,
            name= name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, name, password=None):
        user= self.create_user(email, password, nickname, name)
        user.is_admin= True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id= models.AutoField(primary_key=True)
    email= models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname= models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    name= models.CharField(default='', max_length=100, null=False, blank=False)

    is_active= models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    
    #helper class
    objects= UserManager()

    USERNAME_FIELD='nickname'
    #fields that must needs to be filled
    REQUIRED_FIELDS=['email', 'name']

    def __str__(self):
        return self.nickname

    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value
