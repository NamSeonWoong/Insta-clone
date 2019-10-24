from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model() # User와 같은 기능
        fields = ('email','first_name', 'last_name',)
        
