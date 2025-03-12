from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        if not email:
            raise ValueError('The email field must be set')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, email, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(null=True, default='avatars/default_avatar.png', upload_to='avatars/')
    phone = models.CharField(max_length=20, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    followers = models.ManyToManyField('User', related_name='user_followers', blank=True)
    email = models.EmailField(unique=True)

    # Notifications
    new_message_notification = models.BooleanField(default=False)
    price_change_notification = models.BooleanField(default=False)
    new_offer_notification = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    objects = UserManager()

    def __str__(self):
        return self.username

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, 
    blank=True)
    place = models.CharField(max_length=200, default='Nie podano')

    followers = models.ManyToManyField('User', related_name='offer_followers', blank=True)

    def __str__(self):
        return self.title
