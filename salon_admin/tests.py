from django.test import TestCase, Client
from datetime import datetime
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BeautySalon.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()

from salon.models import Service, Specialist, WorkSchedule


class TestAdminPanel(TestCase):
    def test_services_post(self):
        c = Client()
        response = c.post('/administrator/services/', {'name': 'New test service',
                                                       'price': 200.0,
                                                       'duration': 30})
        self.assertEqual(response.status_code, 200)

    def test_one_service_post(self):
        service = Service.objects.create(name='New Test Service',
                                         price=150.0,
                                         duration=60)
        service.save()

        c = Client()
        response = c.post(f'/administrator/service/{service.id}/', {'name': 'Edited service',
                                                                    'price': 200.0,
                                                                    'duration': 30})
        edited_service = Service.objects.filter(name='Edited service')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(edited_service), 1)

    def test_specialists_post(self):
        c = Client()
        response = c.post('/administrator/specialists/', {'name': 'Halina',
                                                          'phone': '+380994445566',
                                                          'rank': 2})
        self.assertEqual(response.status_code, 302)
        spec = Specialist.objects.filter(phone='+380994445566').first()
        self.assertEqual(spec.name, 'Halina')

    def test_one_specialist(self):
        service = Service.objects.create(name='New Test Service',
                                         price=150.0,
                                         duration=60)
        service.save()
        specialist = Specialist.objects.create(name='Halina',
                                               rank=2,
                                               phone='+380994445566')
        specialist.save()

        c = Client()
        response = c.post(f'/administrator/specialist/{specialist.id}/', {'name': 'Halinka',
                                                                          'phone': '+380994445569',
                                                                          'rank': 2,
                                                                          'status': 2,
                                                                          'begin': '2023-04-10 09:00',
                                                                          'end': '2023-04-10 18:00',
                                                                          f'service_{service.id}': service.id
                                                                          })
        self.assertEqual(response.status_code, 302)

        specialist_schedule = WorkSchedule.objects.filter(specialist=specialist).first()
        self.assertEqual(specialist_schedule.begin_time, datetime(2023, 4, 10, 9, 0))

        specialist_service = Service.objects.filter(specialist__id=specialist.id,
                                                    specialist__workschedule__end_time='2023-04-10 18:00')
        self.assertEqual(len(specialist_service), 1)
