from django.contrib import admin
from django.urls import path,include
from .views import CheckAvailability, view_cart, PlaceEnquiry
from equipments.views import contact

urlpatterns = [
    path('<slug:slug>/<int:pk>/availability', CheckAvailability, name='availability'),
    path('viewcart/', view_cart, name='view_cart'),
    path('contact/', contact, name='contact'),
    path('place_enquiry/', PlaceEnquiry, name='place_enquiry')
]