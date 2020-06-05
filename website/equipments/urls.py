from django.contrib import admin
from django.urls import path,include
from .views import CameraList, LensList, AccessoriesList, EquipmentDetailView, index
from .views import contact
from bookings.views import add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    path('', index, name='home'),
    path('cameras/', CameraList.as_view(), name='cameralist'),
    path('lens/', LensList.as_view(), name='lenslist'),
    path('accessories/', AccessoriesList.as_view(), name='accessorieslist'),
    path('<slug:slug>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    # path('contact/', Contact.as_view(), name='contact'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
]