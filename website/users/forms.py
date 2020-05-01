from users.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):
    
    username = forms.IntegerField(label='',
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            # 'id': 'hi',
        }
))

    
class SignUpForm(UserCreationForm):
    # password1=forms.CharField(max_length=100,required = True)
    # password2=forms.CharField(max_length=100,required = True)
    class Meta:
      model = User  #this is the "YourCustomUser" that you imported at the top of the file  
      fields = ('phone_number','first_name','last_name','password1','password2') #etc etc, other fields you want displayed on the form)  
