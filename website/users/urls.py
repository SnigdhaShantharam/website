from django.contrib import admin
from django.urls import path,include
from .forms import CustomAuthForm
from .views import signup, user_login, contact

urlpatterns = [
    
    # path('login/', auth_views.LoginView.as_view(template_name='equipments/index.html', authentication_form=CustomAuthForm), name='login'),
    path('login/', user_login, name= 'login'),
    path('signup/', signup, name='signup'),
    path('contact/',contact)
]