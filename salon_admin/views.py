from django.shortcuts import render, redirect
from salon.models import Service, Specialist, Booking, WorkSchedule
from salon.views import CURRENT_TIME


def main(request):
    return render(request, 'salon_admin/main.html', {'title': 'Administration page'})


def bookings(request):
    return render(request, 'salon_admin/bookings.html', {'title': 'Bookings page'})


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
    return render(request, 'salon_admin/services.html', {'title': 'Services',
                                                         'services': all_services})


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
    return render(request, 'salon_admin/specialists.html', {'title': 'Specialists',
                                                            'specialists': all_specialist})


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
                                                      begin_time__gte=CURRENT_TIME).order_by('begin_time')
    return render(request, 'salon_admin/specialist.html', {'specialist': specific_specialist,
                                                           'services': all_services,
                                                           'checked_ids': checked_ids,
                                                           'schedules': specialist_schedule})
