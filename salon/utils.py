from datetime import timedelta, datetime

possible_booking_time = []


def calc_possible_time_in_day(serv_duration, start_time, end_time, booked_time):
    """
    Calculate possible order time
    Args:
        serv_duration: int - duration of service, in minutes
        start_time: datetime - start specialist's working time
        end_time: datetime - end specialist's working time
        booked_time: datetime - specialist's booked time
    Returns:
        list of string values - possible booking time
    """
    if end_time <= start_time:
        raise AttributeError('An incorrect datetime values was received')

    duration = timedelta(minutes=serv_duration)
    time_step = timedelta(minutes=15)
    number_of_time_slots = []
    free_time = []

    while start_time <= end_time - duration:
        number_of_time_slots.append(start_time)
        start_time += time_step

    for slot_from in number_of_time_slots:
        if len(booked_time) > 0:
            for booking in booked_time:
                slot_to = slot_from + duration
                if slot_from < booking[1] and slot_to > booking[0] \
                        or slot_from < booking[1] < slot_to:

                    slot_to_add = slot_from.strftime('%Y-%m-%d %H:%M')
                    if slot_to_add in free_time:
                        free_time.remove(slot_to_add)
                    if slot_from > booking[1]:
                        booked_time.remove(booking)
                    break
                else:
                    if slot_from > datetime.today():
                        slot_to_add = slot_from.strftime('%Y-%m-%d %H:%M')
                        if slot_to_add not in free_time:
                            free_time.append(slot_to_add)
        else:
            if slot_from > datetime.today():
                slot_to_add = slot_from.strftime('%Y-%m-%d %H:%M')
                if slot_to_add not in free_time:
                    free_time.append(slot_to_add)

    return free_time
