from users.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class SignUpForm(UserCreationForm):
    # password1=forms.CharField(max_length=100,required = True)
    # password2=forms.CharField(max_length=100,required = True)
    class Meta:
      model = User  #this is the "YourCustomUser" that you imported at the top of the file  
      fields = ('phone_number','first_name','last_name','password1','password2') #etc etc, other fields you want displayed on the form)  