from django.contrib import admin
from django.urls import path,include
from .views import CameraList, LensList, AccessoriesList, index, EquipmentDetailView

urlpatterns = [
    path('', index, name='home'),
    path('cameras/', CameraList.as_view(), name='cameralist'),
    path('lens/', LensList.as_view(), name='lenslist'),
    path('accessories/', AccessoriesList.as_view(), name='accessorieslist'),
    path('<slug:slug>/', EquipmentDetailView.as_view(), name='equipment-detail'),
]