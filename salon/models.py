from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=250, unique=True)
    price = models.FloatField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class Specialist(models.Model):
    RANKS = (
        (1, 'Rank 1'),
        (2, 'Rank 2')
    )
    STATUSES = (
        (1, 'Day off'),
        (2, 'At Work'),
        (3, 'Sickness'),
        (9, 'Fired')
    )
    name = models.CharField(max_length=150, null=False)
    rank = models.IntegerField(default=0, choices=RANKS)
    phone = models.CharField(max_length=20, null=False)
    status = models.IntegerField(default=1, choices=STATUSES)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name


class WorkSchedule(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __repr__(self):
        return f'{Specialist.name} works in {self.date} from {self.begin_time} to {self.end_time}'


class Booking(models.Model):
    STATUSES = (
        (2, 'Accepted'),
        (3, 'Refused'),
        (9, 'Inactive')
    )
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.IntegerField(null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    phone = models.CharField(max_length=20)
    status = models.IntegerField(default=1, choices=STATUSES)

    def __repr__(self):
        return f'Booking: Customer: {self.customer}, ' \
               f'specialist: {Specialist.name}, ' \
               f'date: {self.date}, time: {self.time}'

    def __str__(self):
        return self.customer
