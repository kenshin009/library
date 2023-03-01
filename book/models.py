from django.db import models
from phone_field import PhoneField
from datetime import datetime,date,timedelta
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
# Create your models here.

class User(AbstractUser):
    
    phone =  PhoneField(blank=True,null=True, help_text='Contact phone number')
    address = models.CharField(max_length=250,blank=True,null=True)

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Book(models.Model):

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='')
    image = models.ImageField(upload_to='book_images')
    buy_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

class HireBook(models.Model):

    username = models.CharField(max_length=200,default='')
    book_id = models.IntegerField(default=0)
    hire_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()

    def __str__(self):
        return self.book_name

class WishList(models.Model):

    username = models.CharField(max_length=200,default='')
    book_id = models.IntegerField(default=0)

    def __str__(self):
        return self.username