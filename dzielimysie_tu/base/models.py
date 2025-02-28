from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings   

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default='avatars/default_avatar.png', upload_to='avatars/')

    # USERNAME_FIELD - the field that is used to log in using the email, standard authentication is the username, so if we want to use the email, we need to change it or change authentication backend
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Category(models.Model):
    name = models.CharField(max_length=200)
    offers = models.ManyToManyField('Offer', related_name='categories')

    def __str__(self):
        return self.name
    
class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    place = models.CharField(max_length=200, default='Kr')

    # Figure out how to upload photos 
    # photos = models.ImageField(upload_to='offer_photos/', null=True, blank=True)
    
    # models.CASCADE - when the user is deleted, all offers are deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    body = models.TextField(max_length=100)

    # auto_now_add - when the message is created, the date is added
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # -created - ascending order
        ordering = ['-created']

    def __str__(self):
        return self.body
