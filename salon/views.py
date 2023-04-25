from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import Profile
from django.shortcuts import render, redirect
from salon.models import Service, Specialist, Booking, WorkSchedule
from datetime import datetime, timedelta
from salon.utils import calc_possible_time_in_day
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

    try:
        service_details = Service.objects.filter(name=service_name).first()
        service_id = service_details.id
        service_duration = service_details.duration

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
            available_booking = []
            work_day = WorkSchedule.objects.filter(specialist_id=specialist['id'],
                                                   end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                                   ).values('begin_time', 'end_time').order_by('begin_time')

            for period in work_day:
                booked_time_list = []
                booked_time = Booking.objects.filter(specialist_id=specialist_id,
                                                     booking_to__range=(period['begin_time'], period['end_time'])
                                                     ).values('booking_from', 'booking_to').order_by('booking_from')

                for busy in booked_time:
                    booked_time_list.append([busy['booking_from'], busy['booking_to']])

                free_time = calc_possible_time_in_day(serv_duration=service_duration,
                                                      start_time=period['begin_time'],
                                                      end_time=period['end_time'],
                                                      booked_time=booked_time_list)
                available_booking.extend(free_time)
            specialist.update({'available_booking': available_booking})
    except Exception as err:
        print(f'An error occurred in "One_service" function error:\n{err}')

    return render(request, 'salon/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists})


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
    if request.method == 'POST':
        comment = request.POST['comment']
        booking_from = request.POST['booking_time']

        try:
            service = Service.objects.filter(name=service_name).get()
            user_profile = Profile.objects.filter(user_id=request.user.pk).get()
            user = User.objects.filter(id=request.user.pk).get()

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
            print(f'Booking saving error:\n{err}')
    return redirect('one_service', service_name, specialist_id)


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
