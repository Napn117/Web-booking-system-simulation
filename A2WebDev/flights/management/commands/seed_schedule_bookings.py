from django.core.management.base import BaseCommand
from A2WebDev.flights.models import Aircraft, Airport, Flights, Booking
from datetime import datetime, timedelta
import pytz, csv, random

# This file is used to seed the database with all the necessary objects for 26weeks ahead
# so we can create a realworld simulation for our assignment. We populate random bookings to our
# database after reading in the csv file."""


class Command(BaseCommand):
    help = "Seed the fixed 26-week flight schedule"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding flight schedule...")
        self.seed_schedule(weeks=26)
        self.stdout.write(self.style.SUCCESS("Flight schedule seeded with random bookings provided from the CSV."))

    def seed_schedule(self, weeks=26):
        today = datetime.today().date()
        base_date = today - timedelta(days=today.weekday())



        aircraft = {
            "SyberJet": Aircraft.objects.get(icao="SYBJ1"),
            "Cirrus1": Aircraft.objects.get(icao="CRSJ1"),
            "Cirrus2": Aircraft.objects.get(icao="CRSJ2"),
            "Honda1": Aircraft.objects.get(icao="HDAJ1"),
            "Honda2": Aircraft.objects.get(icao="HDAJ2"),
        }

        airport = {
            "NZNE": Airport.objects.get(icao="NZNE"),
            "YMML": Airport.objects.get(icao="YMML"),
            "NZRO": Airport.objects.get(icao="NZRO"),
            "NZGB": Airport.objects.get(icao="NZGB"),
            "NZCI": Airport.objects.get(icao="NZCI"),
            "NZTL": Airport.objects.get(icao="NZTL"),
        }

        # This is a helper function to add a single flight instance to our database.
        def add_flight(flight_number, aircraft_obj, origin, dest, dep_time, arr_time, price):
            Flights.objects.create(
                flight_number=flight_number,
                aircraft=aircraft_obj,
                origin=origin,
                destination=dest,
                departure_time=dep_time.astimezone(pytz.utc),
                arrival_time=arr_time.astimezone(pytz.utc),
                price=price
            )

        nz_tz = pytz.timezone("Pacific/Auckland")
        aus_tz = pytz.timezone("Australia/Melbourne")
        chatham_tz = pytz.timezone("Pacific/Chatham")

        # Schedule for the Syberjet weekly prestige service. Depart Monday from DF to Melb, and return from
        # Melb on sunday to DF.
        for week in range(weeks):
            week_start = base_date + timedelta(weeks=week)
            friday = week_start + timedelta(days=(4 - week_start.weekday()) % 7)
            sunday = friday + timedelta(days=2)

            dep_nz = nz_tz.localize(datetime.combine(friday, datetime.strptime("10:00", "%H:%M").time()))
            arr_mel = dep_nz + timedelta(hours=3.5)

            dep_mel = aus_tz.localize(datetime.combine(sunday, datetime.strptime("15:00", "%H:%M").time()))
            arr_nz = dep_mel + timedelta(hours=3)

            add_flight(f"DF{week}MEL", aircraft["SyberJet"], airport["NZNE"], airport["YMML"], dep_nz, arr_mel, 1200)
            add_flight(f"MEL{week}DF", aircraft["SyberJet"], airport["YMML"], airport["NZNE"], dep_mel, arr_nz, 1200)


        # Schedule for Honda1 Jet 2x weekly return to Chatham islands. Tues and Fri departing from DF, returning
        # from Chatham Islands to DF on Wed and Sat.
        out_days = [1, 4]
        ret_days = [2, 5]

        for week in range(weeks):
            for i in range(2):
                out_day = base_date + timedelta(weeks=week, days=out_days[i])
                ret_day = base_date + timedelta(weeks=week, days=ret_days[i])

                dep_out = nz_tz.localize(datetime.combine(out_day, datetime.strptime("08:00", "%H:%M").time()))
                arr_out = dep_out + timedelta(hours=2)

                dep_ret = chatham_tz.localize(datetime.combine(ret_day, datetime.strptime("10:00", "%H:%M").time()))
                arr_ret = dep_ret + timedelta(hours=2)

                add_flight(f"CH{week}{i}A", aircraft["Honda1"], airport["NZNE"], airport["NZCI"], dep_out, arr_out, 800)
                add_flight(f"CH{week}{i}B", aircraft["Honda1"], airport["NZCI"], airport["NZNE"], dep_ret, arr_ret, 800)


        # Schedule for Cirrus1 Jet weekday service from DF to Rotorua. Mon-Fri service which departs morning and
        # returns shortly after, repeating this in the afternoon.
        cirrus_days = [0, 1, 2, 3, 4]

        for week in range(weeks):
            for day_offset in cirrus_days:
                day = base_date + timedelta(weeks=week, days=day_offset)

                dep_morning = nz_tz.localize(datetime.combine(day, datetime.strptime("07:00", "%H:%M").time()))
                arr_morning = dep_morning + timedelta(hours=1)
                ret_morning = arr_morning + timedelta(minutes=30)
                arr_back_morning = ret_morning + timedelta(hours=1)

                add_flight(f"RT{week}{day_offset}A", aircraft["Cirrus1"], airport["NZNE"], airport["NZRO"], dep_morning,
                           arr_morning, 300)
                add_flight(f"RT{week}{day_offset}B", aircraft["Cirrus1"], airport["NZRO"], airport["NZNE"], ret_morning,
                           arr_back_morning, 300)

                dep_afternoon = nz_tz.localize(datetime.combine(day, datetime.strptime("16:00", "%H:%M").time()))
                arr_afternoon = dep_afternoon + timedelta(hours=1)
                ret_evening = arr_afternoon + timedelta(minutes=30)
                arr_back_evening = ret_evening + timedelta(hours=1)

                add_flight(f"RT{week}{day_offset}C", aircraft["Cirrus1"], airport["NZNE"], airport["NZRO"],
                           dep_afternoon, arr_afternoon, 300)
                add_flight(f"RT{week}{day_offset}D", aircraft["Cirrus1"], airport["NZRO"], airport["NZNE"], ret_evening,
                           arr_back_evening, 300)


        # Schedule for Honda2 Jet weekly service DF to Lake Tekapo. Flys once at monday from DF and returns back from
        # Lake Tekapo the day after.
        for week in range(weeks):
            mon = base_date + timedelta(weeks=week, days=(0 - base_date.weekday()) % 7)
            tue = mon + timedelta(days=1)

            dep_mon = nz_tz.localize(datetime.combine(mon, datetime.strptime("13:00", "%H:%M").time()))
            arr_mon = dep_mon + timedelta(hours=2)

            dep_tue = nz_tz.localize(datetime.combine(tue, datetime.strptime("14:00", "%H:%M").time()))
            arr_tue = dep_tue + timedelta(hours=2)

            add_flight(f"TK{week}A", aircraft["Honda2"], airport["NZNE"], airport["NZTL"], dep_mon, arr_mon, 600)
            add_flight(f"TK{week}B", aircraft["Honda2"], airport["NZTL"], airport["NZNE"], dep_tue, arr_tue, 600)



        # Schedule for Cirrus2 Jet to Great Barrier Island. Leaves DF mon, wed and fri, which returns back the
        # following respective day to DF.
        out_days2 = [0, 2, 4]
        ret_days2 = [1, 3, 5]

        for week in range(weeks):
            for i in range(3):
                out_day = base_date + timedelta(weeks=week, days=out_days2[i])
                ret_day = base_date + timedelta(weeks=week, days=ret_days2[i])

                dep_out = nz_tz.localize(datetime.combine(out_day, datetime.strptime("09:00", "%H:%M").time()))
                arr_out = dep_out + timedelta(hours=1)

                dep_ret = nz_tz.localize(datetime.combine(ret_day, datetime.strptime("09:00", "%H:%M").time()))
                arr_ret = dep_ret + timedelta(hours=1)

                add_flight(f"GB{week}{i}A", aircraft["Cirrus2"], airport["NZNE"], airport["NZGB"], dep_out, arr_out,
                           450)
                add_flight(f"GB{week}{i}B", aircraft["Cirrus2"], airport["NZGB"], airport["NZNE"], dep_ret, arr_ret,
                           450)

        self.stdout.write("Seeding random bookings...")


        # Read in the csv provided and fill the database with random bookings across the seeded flights.
        passengers = []
        with open('randomnames.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 6:
                    name = f"{row[2]} {row[3]}"
                    email = row[5]
                    passengers.append((name, email))

        all_flights = list(Flights.objects.all())

        for flight in all_flights:
            available_seats = flight.aircraft.capacity
            num_bookings = random.randint(0, available_seats)

            for _ in range(num_bookings):
                if passengers:
                    name, email = random.choice(passengers)
                    Booking.objects.create(
                        flight=flight,
                        passenger_name=name,
                        passenger_email=email
                    )

        self.stdout.write(self.style.SUCCESS("Random bookings created."))
