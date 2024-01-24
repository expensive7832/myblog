from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomizeUser

class securityQuestion(models.Model):
    title = models.CharField(max_length=100)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="profile", default="profile/user.webp")
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=255)
    answer =  models.TextField(max_length=255)

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomizeUser()

    def __str__(self):
        return self.email
    

class PostImage(models.Model):
    image = models.ImageField(upload_to="post")

    def __str__(self):
        return self.image.name

class category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    dateCreated = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    cat = models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ManyToManyField(PostImage, blank=True, null=True)
    desc = models.TextField()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    datePosted = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField("Replies")
   

    def __str__(self):
        return self.message[0:10]


class Replies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    datePosted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[0:10]
