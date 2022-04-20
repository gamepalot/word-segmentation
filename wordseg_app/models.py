from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from enum import auto
from django.db import models
from django.urls import reverse

class User(AbstractUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'password']

    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    # def get_absolute_url(self):
    #     return reverse('user_profile', kwargs={'pk': self.pk})
    
    class Meta:
        db_table = 'users'
        
        
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    project_create_date = models.DateTimeField(auto_now_add=True)
    project_segmentater = models.CharField(max_length=100)
    is_deleted = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return self.project_name
    
    class Meta :
        db_table = 'projects'
        



class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name_ori = models.CharField(max_length=100)
    file_name_encrypt = models.CharField(max_length=100)
    file_type = models.CharField(max_length=100)
    word_upload = models.CharField(max_length=100)
    word_now = models.CharField(max_length=100)
    is_segmented = models.SmallIntegerField(default=0)
    is_deleted = models.SmallIntegerField(default=0)
    versions = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    file_project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.file_name_encrypt
    
    class Meta :
        db_table = 'files'


class Version(models.Model):
    version_id = models.AutoField(primary_key=True)
    version_files = models.TextField()
    version_index = models.IntegerField(default=0)
    version_date = models.DateTimeField(auto_now_add=True)
    version_file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.version_name
    
    class Meta :
        db_table = 'versions'
        
        
class Action(models.Model):
    action_id = models.AutoField(primary_key=True)
    action_index = models.IntegerField(default=0)
    action_date = models.DateTimeField(auto_now_add=True)
    action_version_id = models.ForeignKey(Version, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.action_id
    
    class Meta :
        db_table = 'actions'