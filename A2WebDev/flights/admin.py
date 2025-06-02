from django.contrib import admin
from .models import Airport, Aircraft, Flights, Booking

# Register your models here.

admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(Flights)
admin.site.register(Booking)
