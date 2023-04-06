from django.test import TestCase
from salon.utils import calc_possible_time_in_day
from datetime import datetime

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BeautySalon.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()


class TestCalcPossibleTime(TestCase):
    def test_calc_possible_time_in_day_Equal_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:15', '2023-04-06 09:30']
        self.assertEqual(result, expected_result)

        end_period = datetime.strptime('2023-04-06 13:00', '%Y-%m-%d %H:%M')
        serv_duration = 60
        booked_time = [
            [datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 11:00', '%Y-%m-%d %H:%M')]
        ]
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:00', '2023-04-06 11:00', '2023-04-06 11:15',
                           '2023-04-06 11:30', '2023-04-06 11:45', '2023-04-06 12:00']
        self.assertEqual(result, expected_result)

    def test_calc_possible_time_in_day_List_of_string_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:15', '2023-04-06 09:30']
        self.assertTrue(result, expected_result)

    def test_calc_possible_time_in_day_Wrong_step_value(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:10','2023-04-06 09:15', '2023-04-06 09:30', '2023-04-06 09:40']
        self.assertNotIn(result, expected_result)

    def test_calc_possible_time_in_day_Raise_incorrect_input_period(self):
        end_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        start_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        with self.assertRaises(AttributeError):
            calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)

    def test_calc_possible_time_in_day_Empty_booked_list(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = []
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:00', '2023-04-06 09:15', '2023-04-06 09:30']
        self.assertEqual(result, expected_result)

    def test_calc_possible_time_in_day_Empty_free_time_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:45', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-06 09:45', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = calc_possible_time_in_day(serv_duration, start_period, end_period, booked_time)
        expected_result = []
        self.assertEqual(result, expected_result)
