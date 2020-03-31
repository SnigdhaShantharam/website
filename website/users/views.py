from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from users.forms import SignUpForm
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        # print(form.erorrs)
        if form.is_valid():
            form.save()
            # phonenumber = form.cleaned_data.get('phonenumber')
            # raw_pass = make_password(form.cleaned_data.get('password'))
            # user = authenticate(phonenumber=phonenumber, password=raw_pass)
            # login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            # print("ergwr")
            return redirect("signup")
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})