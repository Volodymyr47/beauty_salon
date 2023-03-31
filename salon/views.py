from django.shortcuts import render, redirect
from salon.models import Service, Specialist, Booking
from datetime import datetime, timedelta


TIMEDELTA = timedelta(days=7)
CURRENT_TIME = datetime.today()
REQUIRED_PERIOD = CURRENT_TIME + TIMEDELTA


def home(request):
    return render(request, 'salon/home.html')


def services(request):
    all_services = {}
    try:
        all_services = Service.objects.filter(specialist__status=2,
                                              specialist__workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                              ).distinct().order_by('name')
    except Exception as err:
        print(err)

    return render(request, 'salon/services.html', {'services': all_services})


def one_service(request, service_name):
    service_id = None
    service_details = {}
    available_specialists = {}
    try:
        service_details = Service.objects.filter(name=service_name).all()
        for detail in service_details:
            service_id = detail.id
        available_specialists = \
            Specialist.objects.filter(status=2,
                                      services__id=service_id,
                                      workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                      ).distinct().order_by('name')
    except Exception as err:
        print(err)

    return render(request, 'salon/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists})


def specialists(request):
    available_specialists = {}

    try:
        available_specialists = Specialist.objects.filter(status=2).distinct()
    except Exception as err:
        print(err)

    return render(request, 'salon/specialists.html', {'specialists': available_specialists})


def one_specialist(request, specialist_id):
    specialist_detail = {}

    try:
        specialist_detail = Specialist.objects.filter(status=2,
                                                      id=specialist_id
                                                      ).first()
    except Exception as err:
        print(err)

    return render(request, 'salon/specialist.html', {'specialist': specialist_detail})


def booking(request, service_name, specialist_id):
    if request.method == 'POST':
        try:
            service = Service.objects.filter(name=service_name).get()
            service_duration = service.duration
            comment = request.POST['comment']
            booking_from = request.POST['booking_time']
            booking_to = datetime.strptime(booking_from, '%Y-%m-%dT%H:%M') + timedelta(minutes=service_duration)

            current_booking = Booking(customer=1,
                                      phone='+380991234556',
                                      status=2,
                                      service_id=service.id,
                                      specialist_id=specialist_id,
                                      booking_from=booking_from,
                                      booking_to=booking_to,
                                      comment=comment)
            current_booking.save()
            return render(request, 'salon/booking-success.html')
        except Exception as err:
            print(f'Booking saving error:\n{err}')
            return redirect(one_service, service_name)
