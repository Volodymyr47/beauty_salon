from django.test import TestCase, Client
from salon.utils import calc_possible_time_in_day
from datetime import datetime

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BeautySalon.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()
from salon.models import Service, Specialist, Booking


class TestCalcPossibleTime(TestCase):

    def test_calc_possible_time_in_day_Equal_result(self):
        start_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M')]
        ]

        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-30 09:15', '2023-04-30 09:30']

        self.assertEqual(result, expected_result)

        end_period = datetime.strptime('2023-04-30 13:00', '%Y-%m-%d %H:%M')
        serv_duration = 60
        booked_time = [
            [datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 11:00', '%Y-%m-%d %H:%M')]
        ]
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-30 09:00', '2023-04-30 11:00', '2023-04-30 11:15',
                           '2023-04-30 11:30', '2023-04-30 11:45', '2023-04-30 12:00']
        self.assertEqual(result, expected_result)

    def test_calc_possible_time_in_day_List_of_string_result(self):
        start_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-30 09:15', '2023-04-30 09:30']
        self.assertTrue(result, expected_result)

    def test_calc_possible_time_in_day_Wrong_step_value(self):
        start_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-30 09:10', '2023-04-30 09:15', '2023-04-30 09:30', '2023-04-30 09:40']
        self.assertNotIn(result, expected_result)

    def test_calc_possible_time_in_day_Raise_incorrect_input_period(self):
        end_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        start_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        with self.assertRaises(AttributeError):
            calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)

    def test_calc_possible_time_in_day_Empty_booked_list(self):
        start_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = []
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-30 09:00', '2023-04-30 09:15', '2023-04-30 09:30']
        self.assertEqual(result, expected_result)

    def test_calc_possible_time_in_day_Empty_free_time_result(self):
        start_period = datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-30 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-30 09:15', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 09:45', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-30 09:45', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-30 10:00', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = []
        self.assertEqual(result, expected_result)


class TestEndpoint(TestCase):
    fixtures = ['../fixtures_for_test.json']

    def setUp(self):
        self.c = Client()

    def test_booking_status_200(self):

        self.c.login(username='vova', password='1')

        service = Service.objects.get(name='Hair cutting')
        specialist = Specialist.objects.get(name='Julia')

        response = self.c.post(f'/booking/{service.name}/{specialist.id}/', {'booking_time': '2023-04-10 10:00',
                                                                             'comment': 'Test comment'})
        self.assertEqual(response.status_code, 302)

        booking = Booking.objects.get(specialist=specialist, service=service)
        self.assertEqual(booking.booking_from, datetime(2023, 4, 10, 10, 0))
