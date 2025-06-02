from django.db import models
import uuid

class Aircraft(models.Model):
    name = models.CharField(max_length=100)
    icao = models.CharField(max_length=5, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.icao})"

class Airport(models.Model):
    name = models.CharField(max_length=100)
    icao = models.CharField(max_length=5, unique=True)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.icao})"

class Flights(models.Model):
    flight_number = models.CharField(max_length=10)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    origin  = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    destination = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} - {self.origin.icao} to {self.destination.icao}"

class Booking(models.Model):
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    time_booked = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=15, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = (uuid.uuid4()).hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passenger_name} booked {self.flight.flight_number}"

