from django.contrib import admin
from .models import Room, Client, Service, Post, Staff, Booking, ProvidedService

admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Post)
admin.site.register(Staff)
admin.site.register(Booking)
admin.site.register(ProvidedService)