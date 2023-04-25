from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from user.utils import salon_admin_required
from salon.models import Service, Specialist, Booking, WorkSchedule
from salon import views as salon_view


def login_redirect(request):
    return render(request, 'salon_admin/login_redirect.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect(admin_home)


@login_required(login_url='/administrator/login/')
@salon_admin_required
def admin_home(request):
    return render(request, 'salon_admin/main.html', {'title': 'Administration page'})


@login_required(login_url='/administrator/login_redirect/')
@salon_admin_required
def bookings(request):
    existing_bookings = Booking.objects.filter(specialist__in=Specialist.objects.all(),
                                               service_id__in=Service.objects.all(),
                                               customer__in=User.objects.all()
                                               ).order_by('-id')
    per_page = 4
    paginator = Paginator(existing_bookings, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'salon_admin/bookings.html', {'title': 'Bookings page',
                                                         'page_obj': page_obj})


@login_required(login_url='/administrator/login_redirect/')
@salon_admin_required
def services(request):
    if request.method == 'POST':
        service_name = request.POST['name']
        service_price = request.POST['price']
        service_duration = request.POST['duration']
        try:
            new_service = Service(name=service_name,
                                  price=service_price,
                                  duration=service_duration)
            new_service.save()
        except Exception as err:
            print(f'New service adding error:\n{err}')

    all_services = Service.objects.all().order_by('name')
    per_page = 3
    paginator = Paginator(all_services, per_page=per_page)
    page_number = request.GET.get('page')
    services_page = paginator.get_page(page_number)
    return render(request, 'salon_admin/services.html', {'title': 'Services',
                                                         'services_page': services_page})


@login_required(login_url='/administrator/login_redirect/')
@salon_admin_required
def one_service(request, service_id):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        duration = request.POST['duration']
        try:
            edited_service = Service.objects.filter(id=service_id).get()
            edited_service.name = name
            edited_service.price = price
            edited_service.duration = duration
            edited_service.save()
            return redirect(services)
        except Exception as err:
            print(f'Saving error of edited service:\n{err}')

    specific_service = Service.objects.filter(id=service_id).get()
    return render(request, 'salon_admin/service.html', {'service': specific_service})


@login_required(login_url='/administrator/login_redirect/')
@salon_admin_required
def specialists(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        rank = request.POST['rank']
        status = 2
        try:
            new_specialist = Specialist(name=name,
                                        phone=phone,
                                        rank=rank,
                                        status=status)
            new_specialist.save()
            return redirect(specialists)
        except Exception as err:
            print(f'New specialist adding error:\n{err}')

    all_specialist = Specialist.objects.all()
    per_page = 3
    paginator = Paginator(all_specialist, per_page=per_page)
    page_number = request.GET.get('page')
    specialists_page = paginator.get_page(page_number)

    return render(request, 'salon_admin/specialists.html', {'title': 'Specialists',
                                                            'specialists_page': specialists_page})


@login_required(login_url='/administrator/login_redirect/')
@salon_admin_required
def one_specialist(request, specialist_id):
    checked_services = Service.objects.filter(specialist__id=specialist_id).all()
    checked_ids = []
    for service in checked_services:
        checked_ids.append(service.id)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        rank = request.POST['rank']
        status = request.POST['status']
        begin_time = request.POST['begin']
        end_time = request.POST['end']
        try:
            specialist = Specialist.objects.filter(id=specialist_id).get()
            specialist.name = name
            specialist.rank = rank
            specialist.phone = phone
            specialist.status = status
            specialist.save()

            if begin_time and end_time:
                work_schedule = WorkSchedule(specialist_id=specialist_id)
                work_schedule.begin_time = begin_time
                work_schedule.end_time = end_time
                work_schedule.save()

            service_ids = [value for key, value in request.POST.items() if key.startswith('service')]

            for one_id in checked_ids:
                specialist.services.remove(one_id)

            for service_id in service_ids:
                service = Service.objects.filter(id=service_id).get()
                specialist.services.add(service)

            specialist.save()
            return redirect(one_specialist, specialist_id)
        except Exception as err:
            print(f'Specialist data update error:\n{err}')

    specific_specialist = Specialist.objects.filter(id=specialist_id).get()
    all_services = Service.objects.all()
    specialist_schedule = WorkSchedule.objects.filter(specialist_id=specialist_id,
                                                      begin_time__gte=salon_view.CURRENT_TIME).order_by('begin_time')
    return render(request, 'salon_admin/specialist.html', {'specialist': specific_specialist,
                                                           'services': all_services,
                                                           'checked_ids': checked_ids,
                                                           'schedules': specialist_schedule})
