from django.shortcuts import render
from django.views.generic import DetailView


def home(request):
    return render(request, 'salon/home.html')


def services(request):
    return render(request, 'salon/services.html')


#
# class SpecificService(DetailView):
#     model = Service
#     template_name = 'salon/service.html'
#     context_object_name = Service.name


def service(request, service_name):
    return render(request, 'salon/service.html', {'title': service_name})


def specialists(request):
    return render(request, 'salon/specialists.html')


def specialist(request, specialist_id):
    return render(request, 'salon/specialists.html', {'title': specialist_id})


def booking(request, user_id, service_name, booking_time):
    if request.method == 'POST':
        pass
    return render(request, 'salon/booking.html', {'title': 'booking'})
