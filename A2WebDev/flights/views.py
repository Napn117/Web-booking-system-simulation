from django.shortcuts import render, get_object_or_404, redirect
from .models import Aircraft, Flights, Booking
from .forms import BookingForm, BookingSearchForm
from datetime import datetime, timedelta
import pytz


# This function is for searching the flights on a chosen date, which can optionally be filtered by jet.
# Timezone is converted into local timezones and shows the flights on the chosen date.
# Available seats are calculated through minusing the bookings from the total seats.
def search_flights(request):
    flights = []
    query_date = request.GET.get('date')
    aircraft_id = request.GET.get('aircraft')
    if query_date:
        try:
            date_obj = datetime.strptime(query_date, '%Y-%m-%d').date()
            utc_start = datetime.combine(date_obj, datetime.min.time()).replace(tzinfo=pytz.utc)
            utc_end = datetime.combine(date_obj, datetime.max.time()).replace(tzinfo=pytz.utc)
            results = Flights.objects.filter(departure_time__range=(utc_start - timedelta(hours=13),
                utc_end + timedelta(hours=13)))
            if aircraft_id:
                results = results.filter(aircraft_id=aircraft_id)

            filtered = []
            for flight in results:
                origin_tz = pytz.timezone(flight.origin.timezone)
                dest_tz = pytz.timezone(flight.destination.timezone)
                local_dt = flight.departure_time.astimezone(origin_tz)
                local_arrival = flight.arrival_time.astimezone(dest_tz)
                if local_dt.date() == date_obj:
                    flight.departure_abbr = local_dt.tzname()
                    flight.arrival_abbr = local_arrival.tzname()
                    flight.seats_available = flight.aircraft.capacity - Booking.objects.filter(flight=flight).count()
                    filtered.append(flight)

            filtered.sort(key=lambda f: f.departure_time)
            flights = filtered
        except ValueError:
            pass  # invalid date format
    context = {
        'flights': flights,
        'aircraft_list': Aircraft.objects.all()
    }
    return render(request, 'search.html', context)



# This function allows the user to make a booking.
# There must be an available seat for a successful booking else we show the user the booking_full page.
# If there are seats, user is directed to booking_success and shown the confirmation.
def book_flight(request, flight_id):
    flight = get_object_or_404(Flights, id=flight_id)
    existing_bookings = Booking.objects.filter(flight=flight).count()
    if existing_bookings >= flight.aircraft.capacity:
        return render(request, 'booking_full.html', {'flight': flight})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.flight = flight
            booking.save()
            return render(request, 'booking_success.html', {'booking': booking})

    else:
        form = BookingForm()
    return render(request, 'book_flight.html', {'form': form, 'flight': flight})


# This function allows a user to search for existing bookings under an email address.
# The user may choose to cancel any bookings listed, which will update for the next time someone searches that flight.
# Anyone can delete a booking knowing the email address, but I don't think security matters for our assignment.
def find_booking(request):
    form = BookingSearchForm(request.GET or None)
    bookings = []
    if form.is_valid():
        email = form.cleaned_data['passenger_email']
        bookings = Booking.objects.filter(passenger_email=email)
        if request.method == "POST":
            booking_id = request.POST.get("cancel_id")
            booking_to_cancel = Booking.objects.filter(id=booking_id, passenger_email=email).first()
            if booking_to_cancel:
                booking_to_cancel.delete()
                return redirect(request.path + f"?passenger_email={email}")

    return render(request, "find_booking.html", {"form": form, "bookings": bookings})