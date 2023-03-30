from django.shortcuts import render
from salon.models import Service, Specialist
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
        available_specialists = Specialist.objects.filter(status=2,
                                                          # workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                                          ).distinct()
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


def booking(request, user_id, service_name, booking_time):
    if request.method == 'POST':
        pass
    return render(request, 'salon/booking.html', {'title': 'booking'})
