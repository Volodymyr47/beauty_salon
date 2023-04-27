from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import Profile
from django.shortcuts import render, redirect
from salon.models import Service, Specialist, Booking
from datetime import datetime, timedelta
from .booking_researcher import get_possible_booking_time
from user.utils import simple_user_required

TIMEDELTA = timedelta(days=7)
CURRENT_TIME = datetime.today()
REQUIRED_PERIOD = CURRENT_TIME + TIMEDELTA


@simple_user_required
def home(request):
    return render(request, 'salon/home.html')


@simple_user_required
def services(request):
    all_services = {}

    try:
        all_services = Service.objects.filter(specialist__status=2,
                                              specialist__workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                              ).distinct().order_by('name')
    except Exception as err:
        print(err)

    return render(request, 'salon/services.html', {'services': all_services})


@simple_user_required
def one_service(request, service_name, specialist_id=None):
    service_details = {}
    available_specialists = {}
    err_time = request.GET.get('err')

    if err_time:
        message = f'Sorry, but time of {err_time} is not more available. ' \
                  f'Please choose the other available time'
    else:
        message = None

    try:
        service_details = Service.objects.get(name=service_name)
        service_id = service_details.id

        if not specialist_id:
            available_specialists = \
                Specialist.objects.filter(status=2,
                                          services__id=service_id,
                                          workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                          ).distinct().values('id', 'name').order_by('name')
        else:
            available_specialists = Specialist.objects.filter(id=specialist_id,
                                                              status=2,
                                                              workschedule__end_time__gt=CURRENT_TIME
                                                              ).distinct().values('id', 'name')

        for specialist in available_specialists:
            specialist_id = specialist['id']
            available_booking = get_possible_booking_time(specialist_id, service_id, REQUIRED_PERIOD)
            specialist.update({'available_booking': available_booking})

    except Exception as err:
        print(f'An error occurred in "One_service" function error:\n{err}')

    return render(request, 'salon/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists,
                                                  'message': message})


@simple_user_required
def specialists(request):
    available_specialists = {}

    try:
        available_specialists = Specialist.objects.filter(status=2,
                                                          workschedule__end_time__gt=CURRENT_TIME).distinct()
    except Exception as err:
        print(err)

    return render(request, 'salon/specialists.html', {'specialists': available_specialists})


@simple_user_required
def one_specialist(request, specialist_id):
    specialist = {}
    available_services = []
    try:
        specialist = Specialist.objects.filter(status=2,
                                               id=specialist_id
                                               ).first()

        available_services = Service.objects.filter(specialist__id=specialist.id).all()
    except Exception as err:
        print(err)

    return render(request, 'salon/specialist.html', {'specialist': specialist,
                                                     'services': available_services})


@login_required(login_url='/user/login')
@simple_user_required
def make_booking(request, service_name, specialist_id):
    message = None

    if request.method == 'POST':
        comment = request.POST['comment']
        booking_from = request.POST['booking_time']

        try:
            service = Service.objects.filter(name=service_name).get()
            user_profile = Profile.objects.filter(user_id=request.user.pk).get()
            user = User.objects.filter(id=request.user.pk).get()

            possible_slot_list = get_possible_booking_time(specialist_id, service.id, REQUIRED_PERIOD)
            if booking_from not in possible_slot_list:
                err_time = booking_from
                # message = f'Sorry, but time of {booking_from} is not more available. ' \
                #           f'Please choose the other available time'
                return redirect(f'/service/{service_name}/{specialist_id}/?err={err_time}')
                # return redirect('one_service', service_name, specialist_id, message)

            service_duration = service.duration
            booking_to = datetime.strptime(booking_from, '%Y-%m-%d %H:%M') + timedelta(minutes=service_duration)

            current_booking = Booking(customer=user,
                                      phone=user_profile.phone,
                                      status=2,
                                      service_id=service.id,
                                      specialist_id=specialist_id,
                                      booking_from=booking_from,
                                      booking_to=booking_to,
                                      comment=comment)
            current_booking.save()
            return HttpResponseRedirect(reverse('booking_success', args=[user.id]))

        except Exception as err:
            message = 'An error occurred during you booking. Please check booking info and try again'
            print(f'Booking saving error:\n{err}')
    return redirect('one_service', service_name, specialist_id, message)


@login_required(login_url='/user/login')
@simple_user_required
def booking_success(request, user_id):
    booked = {}
    try:
        booked = Booking.objects.filter(customer=user_id,
                                        booking_from__gte=CURRENT_TIME,
                                        ).all().order_by('-booking_from')
    except Exception as err:
        print(f'An error occurred in "get_booking_info" function\n{err}')

    if booked:
        per_page = 5
        paginator = Paginator(booked, per_page=per_page)
        page_number = request.GET.get('page')
        booking_page = paginator.get_page(page_number)
        return render(request, 'salon/booking-success.html', {'booking_page': booking_page})
    message = 'You do not have any bookings'
    return render(request, 'salon/booking-success.html', {'message': message})
