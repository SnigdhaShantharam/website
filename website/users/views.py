from django.contrib.auth import login, authenticate, logout
# from django.http import HttpResponse
# from django.contrib.auth.hashers import make_password
# # from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages

from rest_framework.response import Response
from rest_framework import status

from users.forms import SignUpForm, CustomAuthForm
from .models import User

def user_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if user:
            if user.is_active:
                login(request,user)
                # return HttpResponse("Login successfull.", status=status.HTTP_200_OK)
                return redirect('home')
            else:
                return HttpResponse("Account not verified.", status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(phone_number, password))
            return HttpResponse("Invalid credentials", status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, 'equipments/home.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('request.POST', request.POST)
        print()
        print(SignUpForm(request.POST))
        print(form.is_valid())
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
        return render(request, 'equipments/signup.html', {'form': form})

def user_logout(request):
    try:
        # user = request.user
        logout(request)
        # cache.delete(user.username)
        return redirect('home')
    except Exception as e:
        print(e)
       
def contact(request):
    map = User.objects.filter(pk=1).first()
    print(map.location)