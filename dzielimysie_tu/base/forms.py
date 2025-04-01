from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Offer

class My_User_Creation_Form(UserCreationForm):
    class Meta:
        model = User
        # password1 and password2 are built in fields for password and password confirmation
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {'first_name': 'Imię'}

class Offer_Form(ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'
        exclude = ['creator', 'status']
