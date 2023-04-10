from datetime import timedelta, datetime


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

    service_duration = timedelta(minutes=serv_duration)
    time_step = timedelta(minutes=15)
    number_of_time_slots = []
    free_time = []

    while start_time <= end_time - service_duration:
        number_of_time_slots.append(start_time)
        start_time += time_step

    for slot in number_of_time_slots:
        if len(booked_time):
            for booking in booked_time:
                slot_duration = slot + service_duration
                duration = [slot, slot_duration]
                if slot + time_step == booking[1]:
                    booked_time.remove(booking)
                if duration[0] < booking[1] and duration[1] > booking[0] \
                        or duration[0] <= booking[1] < duration[1]:
                    break
                else:
                    if slot > datetime.today():
                        slot_to_add = slot.strftime('%Y-%m-%d %H:%M')
                        free_time.append(slot_to_add)
        else:
            if slot > datetime.today():
                slot_to_add = slot.strftime('%Y-%m-%d %H:%M')
                free_time.append(slot_to_add)
    return free_time
