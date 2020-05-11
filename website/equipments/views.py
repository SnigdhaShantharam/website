from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Equipment
# , Equipment_Images


def index(request):
    if request.method == 'GET':
        return render(request, 'equipments/home.html')

class CameraList(ListView):
    '''
    Summary:
        --------
            get the list of available cameras.
        Methods:
        --------
            get: list of available cameras.
    '''
    model = Equipment
    
    def get_context_data(self):
        qs = Equipment.objects.filter(equipment_type='Camera')
        # print(qs)
        context = {
            'equipment_type': 'Camera',
            'object_list': qs
        }
        return context


class LensList(ListView):
    '''
    Summary:
        --------
            get the list of available lens.
        Methods:
        --------
            get: list of available lens.
    '''
    model = Equipment
    
    def get_context_data(self):
        qs = Equipment.objects.filter(equipment_type='Lens')
        context = {
            'equipment_type': 'Lens',
            'object_list': qs
        }
        return context


class AccessoriesList(ListView):
    '''
    Summary:
        --------
            get the list of available Accessories.
        Methods:
        --------
            get: list of available Accessories.
    '''
    model = Equipment
    
    def get_context_data(self):
        qs = Equipment.objects.filter(equipment_type='Accessories')
        context = {
            'equipment_type': 'Accessories',
            'object_list': qs
        }
        return context

class EquipmentDetailView(DetailView):

    queryset = Equipment.objects.all()

    def get_object(self):
        obj = super().get_object()
        # print(obj)
        return obj
