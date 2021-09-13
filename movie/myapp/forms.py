from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Viewer
class ViewerCreationForm(UserCreationForm):
    password1 = forms.CharField(label = 'Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'Retype Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = Viewer
        fields = ['username','first_name','last_name','dob']
        widgets={
            'dob': forms.DateInput(format = ('%d-%m-%y'),attrs={'class':'form-control', 'type': 'date'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'dob':'Date of Birth'
        }
class LoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Username',widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label = 'Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))

