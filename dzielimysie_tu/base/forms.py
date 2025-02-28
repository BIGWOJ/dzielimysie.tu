from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class My_User_Creation_Form(UserCreationForm):
    class Meta:
        model = User
        # password1 and password2 are built in fields for password and password confirmation
        fields = ['username', 'email', 'password1', 'password2']
