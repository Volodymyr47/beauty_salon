from datetime import datetime

from .models import Service, WorkSchedule, Booking, Specialist
from .utils import calc_possible_time_in_day


def get_possible_booking_time(specialist_id, service_id, required_period):
    """
    Args:
        specialist_id: int - id of available specialist
        service_id: int - id of available service
        required_period: datetime - the max period to show the data of available specialists and services

    Returns: list of string of datetime elements - available booking slots
    """
    possible_booking_time = []
    service = Service.objects.get(id=service_id)
    work_day = WorkSchedule.objects.filter(specialist_id=specialist_id,
                                           end_time__range=(datetime.today(), required_period)
                                           ).values('begin_time', 'end_time').order_by('begin_time')

    for period in work_day:
        booked_time_list = []
        booked_time = Booking.objects.filter(specialist_id=specialist_id,
                                             booking_to__range=(period['begin_time'], period['end_time'])
                                             ).values('booking_from', 'booking_to').order_by('booking_from')

        for busy in booked_time:
            booked_time_list.append([busy['booking_from'], busy['booking_to']])

        free_time = calc_possible_time_in_day(serv_duration=service.duration,
                                              start_time=period['begin_time'],
                                              end_time=period['end_time'],
                                              booked_time=booked_time_list)
        possible_booking_time.extend(free_time)
    return possible_booking_time
