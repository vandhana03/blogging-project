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
    

class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT="Draft"
        PUBLISHED="Published"
        ARCHIVED="Archived"

    title=models.CharField(max_length=250)
    content=models.TextField()
    author=models.ForeignKey(Users,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)

    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f" comment by {self.user.username} on {self.post.title}"
