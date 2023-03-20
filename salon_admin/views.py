from django.shortcuts import render


def main(request):
    return render(request, 'salon_admin/main.html', {'title': 'Administration page'})


def bookings(request):
    return render(request, 'salon_admin/bookings.html', {'title': 'Bookings page'})


def services(request):
    return render(request, 'salon_admin/services.html', {'title': 'Services page'})


def service(request, service_name):
    return render(request, 'salon_admin/services.html', {'title': service_name})


def specialists(request):
    return render(request, 'salon_admin/specialists.html', {'title': 'Specialists page'})


def specialist(request, specialist_id):
    return render(request, 'salon_admin/specialist.html', {'title': f'Specialist ID is {specialist_id}'})
