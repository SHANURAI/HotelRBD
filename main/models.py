# models.py
from django.db import models

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    type = models.TextField()
    cost_per_night = models.IntegerField()

    class Meta:
        db_table = 'Rooms'

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    year_of_birth = models.IntegerField()
    gender = models.CharField(max_length=1)
    username = models.CharField(max_length=100)

    class Meta:
        db_table = 'Clients'

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.TextField()
    cost = models.FloatField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Services'

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    name = models.TextField()
    salary = models.FloatField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Posts'

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    year_of_birth = models.IntegerField()
    gender = models.CharField(max_length=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Staff'

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    count_of_nights = models.IntegerField()
    total_booking_cost = models.FloatField()

    class Meta:
        db_table = 'Bookings'

class ProvidedService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    count_of_services = models.IntegerField()
    total_service_cost = models.FloatField()

    class Meta:
        db_table = 'Provided_Services'
        unique_together = ('booking', 'staff', 'service')