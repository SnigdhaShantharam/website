import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.list import ListView

from equipments.models import Equipment
from users.forms import CustomAuthForm

from . import forms as forms
from .models import EnquiryCart, EnquiryItem, Event
from .utils import (check_availability, formaStrDate, make_log_in_db,
                    send_enquiry_mail)


def view_cart(request):
    # if request.user.is_anonymous():
    #         return render(request, 'equipments/lginredirct.html')
    # elif request.method == 'GET':
    if request.user.is_authenticated:
        try:
            order_qs = EnquiryCart.objects.filter(
                customer=request.user, ordered=False)
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
            make_log_in_db(log_type='failure',
                           reference='viewcart',
                           response={'error': str(e)},
                           request={'request': request})
            # print(e)
    else:
        form = CustomAuthForm()
        return render(request, 'equipments/lginredirct.html', {'heading': 'Please login to continue', 'form': form})


def add_to_cart(request, slug):
    if request.user.is_authenticated:
        try:
            item = get_object_or_404(Equipment, slug=slug)
            enquiry_item, created = EnquiryItem.objects.get_or_create(item=item,
                                                                      customer=request.user,
                                                                      ordered=False)
            order_qs = EnquiryCart.objects.filter(
                customer=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__slug=item.slug).exists():
                    messages.info(request, 'Equipment updated.')
                    # messages.warning('Equipment already in cart')
                else:
                    order.items.add(enquiry_item)
            else:
                enquiry_date = timezone.now()
                order = EnquiryCart.objects.create(
                    customer=request.user, enquiry_date=enquiry_date)
                order.items.add(enquiry_item)

            messages.info(request, 'Equipment added for enquiry.')
            return redirect("equipment-detail", slug=slug)
        except Exception as e:
            make_log_in_db(log_type='failure',
                           reference='add to cart',
                           response={'error': str(e)},
                           request={'request': request})
    else:
        form = CustomAuthForm()
        return render(request, 'equipments/lginredirct.html', {'heading': 'Please login to continue', 'form': form})


def remove_from_cart(request, slug):
    try:
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
    except Exception as e:
        make_log_in_db(log_type='failure',
                       reference='remove to cart',
                       response={'error': str(e)},
                       request={'request': request})


def PlaceEnquiry(request):
    if request.method == 'POST':
        try:
            form = forms.EnquiryForm(request.POST)
            if form.is_valid():
                # form.save()
                enquiry = EnquiryCart.objects.filter(customer=request.user,
                                                     ordered=False
                                                     ).first()

                # print(enquiry.items.all())
                send_enquiry_mail(request, enquiry)
                enquiry.ordered = True
                enquiry.save()
                messages.success(
                    request, 'Enquiry has been placed successfully. You can expect a call for confirmation soon.')
                return HttpResponseRedirect(request.path_info)
                # return redirect(request.path_info, )
        except Exception as e:
            make_log_in_db(log_type='failure',
                           reference='Place_Enqiry',
                           response={'error': str(e)},
                           request={'request': request})
    else:
        form = forms.EnquiryForm(initial={
            'phone_num': request.user.phone_number,
            'Firstname': request.user.first_name,
            'Lastname': request.user.last_name,
            'email': request.user.email
        })
        return render(request, 'equipments/signup.html', {'heading': 'Place an enquiry', 'form': form})


def CheckAvailability(request, pk, slug):

    if request.method == "POST":
        try:
            start_date = formaStrDate(request.POST.get('start_date'))
            end_date = formaStrDate(request.POST.get('end_date'))
            if end_date < start_date:
                msg = "Please check the dates you have entered."
                messages.error(request, msg, extra_tags='danger')
                return HttpResponseRedirect(request.POST.get('previous_page'))
            # print(request.POST.get('previous_page'))
            # print(request.path_info)
            # print(str(start_date))
            else:
                event = Event.objects.filter(
                    Q(start_day__exact=start_date, equipment_key=pk) |
                    Q(start_day__exact=end_date, equipment_key=pk)
                ).order_by('-id')
                if event:
                    event = event[0]
                    status = check_availability(
                        event.start_day, event.end_day, start_date, end_date, event.inventory)
                    if status:
                        # print('yes')https://thumbs.gfycat.com/QuaintLikelyFlyingfish-size_restricted.gif
                        msg = "Product available for {} and {}.".format(
                            str(start_date), str(end_date))
                        messages.success(request, msg)
                        return HttpResponseRedirect(request.POST.get('previous_page'))
                        # return HttpResponse("yes!! available", status=200)
                    else:
                        msg = "Sorry!! Product not available for the dates you are looking for."
                        messages.error(request, msg, extra_tags='danger')
                        # print('no')
                        return HttpResponseRedirect(request.POST.get('previous_page'))
                        # return HttpResponse("not available", status=400)
                else:
                    msg = "Product available for {} and {}.".format(
                        str(start_date), str(end_date))
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.POST.get('previous_page'))
                    # return HttpResponse("yes!! available", status=200)
        except Exception as e:
            make_log_in_db(log_type='failure',
                           reference='check availability',
                           response={'error': str(e)},
                           request={'request': request})
