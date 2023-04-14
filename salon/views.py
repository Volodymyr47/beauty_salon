from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.shortcuts import render, redirect
from salon.models import Service, Specialist, Booking, WorkSchedule
from datetime import datetime, timedelta
from salon.utils import calc_possible_time_in_day

TIMEDELTA = timedelta(days=7)
CURRENT_TIME = datetime.today()
REQUIRED_PERIOD = CURRENT_TIME + TIMEDELTA


def home(request):
    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

    return render(request, 'salon/home.html')


def services(request):
    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

    all_services = {}
    try:
        all_services = Service.objects.filter(specialist__status=2,
                                              specialist__workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                              ).distinct().order_by('name')
    except Exception as err:
        print(err)

    return render(request, 'salon/services.html', {'services': all_services})


def one_service(request, service_name, specialist_id=None):

    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

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
            work_day = WorkSchedule.objects.filter(specialist_id=specialist_id,
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
        print(f'One_service error:\n{err}')

    return render(request, 'salon/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists})


def specialists(request):

    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

    available_specialists = {}

    try:
        available_specialists = Specialist.objects.filter(status=2,
                                                          workschedule__end_time__gt=CURRENT_TIME).distinct()
    except Exception as err:
        print(err)

    return render(request, 'salon/specialists.html', {'specialists': available_specialists})


def one_specialist(request, specialist_id):

    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

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
def booking(request, service_name, specialist_id):

    if request.user.groups.filter(id=1).exists():
        return render(request, 'salon/404.html', status=404)

    if request.method == 'POST':
        comment = request.POST['comment']
        booking_from = request.POST['booking_time']

        try:
            service = Service.objects.filter(name=service_name).get()
            user_profile = Profile.objects.filter(user_id=request.user.pk).get()

            service_duration = service.duration
            booking_to = datetime.strptime(booking_from, '%Y-%m-%d %H:%M') + timedelta(minutes=service_duration)

            current_booking = Booking(customer=user_profile.user_id,
                                      phone=user_profile.phone,
                                      status=2,
                                      service_id=service.id,
                                      specialist_id=specialist_id,
                                      booking_from=booking_from,
                                      booking_to=booking_to,
                                      comment=comment)
            current_booking.save()

            booked = Booking.objects.filter(customer=user_profile.user_id,
                                            booking_from__gte=booking_from,
                                            ).all()
            return render(request, 'salon/booking-success.html', {'booked': booked})
        except Exception as err:
            print(f'Booking saving error:\n{err}')
    return redirect(one_service, service_name, specialist_id)
