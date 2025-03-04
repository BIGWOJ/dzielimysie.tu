from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings   

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default='avatars/default_avatar.png', upload_to='avatars/')
    phone = models.CharField(max_length=20, null=True) 
    place = models.CharField(max_length=100, null=True)
    followers = models.ManyToManyField('User', related_name='user_followers', blank=True)

    # Notifications
    new_message_notification = models.BooleanField(default=False)
    price_change_notification = models.BooleanField(default=False)
    new_offer_notification = models.BooleanField(default=False)

    # USERNAME_FIELD - the field that is used to log in using the email, standard authentication is the username, so if we want to use the email, we need to change it or change authentication backend
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Category(models.Model):
    name = models.CharField(max_length=200)
   
    def __str__(self):
        return self.name
    
class Photo(models.Model):
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='offer_photos/')

    def __str__(self):
        return self.offer.title

class Follow_user(models.Model):
    following_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followed_by')

class Follow_offer(models.Model):
    following_user = models.ForeignKey('User', on_delete=models.CASCADE)
    followed_offer = models.ForeignKey('Offer', on_delete=models.CASCADE)

class Offer(models.Model):
    title = models.CharField(max_length=200)

    # models.CASCADE - when the user is deleted, all their offers are deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creator_name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, 
    blank=True)
    creator_email = models.EmailField(null=True)
    creator_phone = models.CharField(max_length=20, null=True) 
    place = models.CharField(max_length=200, default='Nie podano')

    followers = models.ManyToManyField('User', related_name='offer_followers', blank=True)

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
