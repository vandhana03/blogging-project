from django.db import models

# Create your models here.
class Users(models.Model):
    class Role(models.TextChoices):
        ADMIN="ADMIN"
        USER="USER"
    username=models.CharField(max_length=50,primary_key=True)
    email=models.EmailField(unique=True)
    email_verification = models.BooleanField(default=False)
    password=models.CharField(max_length=150)
    role=models.CharField(max_length=10,choices=Role,default=Role.USER)
    profile_picture=models.URLField(max_length=500,blank=True,null=True)

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    desc=models.TextField()

    def __str__(self):
        return self.name