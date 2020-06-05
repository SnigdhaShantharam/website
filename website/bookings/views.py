from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.list import ListView

import datetime

from . import forms as forms
from .utils import check_availability, formaStrDate
from .models import Event, EnquiryCart, EnquiryItem

from equipments.models import Equipment
from users.forms import CustomAuthForm


def view_cart(request):
    # if request.user.is_anonymous():
    #         return render(request, 'equipments/lginredirct.html')
    # elif request.method == 'GET':  
    if request.user.is_authenticated:  
        try:
            order_qs = EnquiryCart.objects.filter(customer=request.user, ordered=False)
            if not order_qs.exists():
                context = {
                    'message': 'Your enquiry cart is empty...'
                }
            else:
                for i in order_qs:
                    if i.items.all():
                        context = {
                    'message': 'You have added the following gadgets for enquiry :',
                    'objects': EnquiryCart.objects.filter(customer=request.user, ordered=False)
                }
                    else:
                        context = {
                        'message': 'Your enquiry cart is empty...'
                    }
                
            return render(request, 'bookings/view_cart.html', context=context)
        except Exception as e:
            print(e)
    else:
        form = CustomAuthForm()
        return render(request, 'equipments/lginredirct.html', {'heading': 'Please login to continue','form': form})

def add_to_cart(request, slug):
    item = get_object_or_404(Equipment, slug=slug)
    enquiry_item, created = EnquiryItem.objects.get_or_create(item=item,
                                                    customer=request.user,
                                                    ordered=False)
    order_qs = EnquiryCart.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            messages.info(request, 'Equipment updated.')
            # messages.warning('Equipment already in cart')
        else:
            order.items.add(enquiry_item)
    else:
        enquiry_date = timezone.now()
        order = EnquiryCart.objects.create(customer=request.user, enquiry_date=enquiry_date)
        order.items.add(enquiry_item)
        
    messages.info(request, 'Equipment added for enquiry.')
    return redirect("equipment-detail", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Equipment, slug=slug)
    order_qs = EnquiryCart.objects.filter(customer=request.user,
                                        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            # messages.warning(request, 'Equipment already in cart')
            enquiry_item = EnquiryItem.objects.filter(item=item,
                                                    customer=request.user,
                                                    ordered=False)[0]
            order.items.remove(enquiry_item)
            order.save()
            # messages.error(request, 'Equipment was removed from the enquiry.')
            return redirect("view_cart")
        else:
            messages.error(request, 'Cart does not contain the equipment')
            return redirect("view_cart")
    else:
        messages.error(request, 'you do not have an active order')
        return redirect("view_cart")
    return redirect("view_cart")

def PlaceEnquiry(request):
    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        print('request.POST', request.POST)
        print(form)
        print(form.is_valid())
        # print(form.erorrs)
        if form.is_valid():
            form.save()
            return redirect("place_enquiry")
    else:
        form = forms.EnquiryForm()
        return render(request, 'equipments/signup.html', {'heading':'Place an enquiry','form': form})
    pass

def CheckAvailability(request, pk, slug):
    
    if request.method == "POST":
        start_date = formaStrDate(request.POST.get('start_date'))
        end_date = formaStrDate(request.POST.get('end_date'))
        print(request.POST)
        # print(start_date)
        event = Event.objects.filter(
            Q(start_day__exact=start_date, equipment_key=pk)|
            Q(start_day__exact=end_date, equipment_key=pk)
            ).order_by('-id')[0]
        if event:
            print(event)
            status = check_availability(event.start_day, event.end_day, start_date, end_date, event.inventory)
            if status:
                print('yes')
                messages.success(request, "is available")
                return HttpResponse("yes!! available", status=200)
            else:
                messages.error(request, "Sorry!! Product not available for the dates you are looking for.")
                print('no')
                return HttpResponse("not available", status=400)
        else:
            print('available')
            return HttpResponse(status=200)