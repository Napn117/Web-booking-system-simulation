# ✈️ Dairy Flat Airline Booking System – 159.352 Assignment 2

## 📘 Overview

This project implements a web-based **online flight booking system** for a fictional airline based at Dairy Flat Airport. It supports searching for scheduled flights, booking seats, viewing bookings, and cancelling reservations. The system is designed to handle multiple aircraft, routes, and time zones.

---

## ✅ Features

- **Landing page** with navigation to search and booking tools
- **Flight search** by origin, destination, and date
- **Booking system** allowing seat selection and confirmation
- **Booking cancellation** with secure lookup by reference ID
- **Timezone-aware scheduling** for all supported destinations
- Fully seeded flight schedule based on a weekly timetable

---

## 🛫 Routes & Aircraft

The following aircraft and routes are supported:

| Aircraft           | Capacity | Route                               | Frequency                          |
|--------------------|----------|--------------------------------------|------------------------------------|
| SyberJet SJ30i     | 6        | Dairy Flat ↔ Melbourne (YMML)        | Weekly (Fri outbound, Sun return)  |
| Cirrus SF50 (x2)   | 4        | Dairy Flat ↔ Rotorua (NZRO)          | Twice daily (Mon–Fri)              |
| Cirrus SF50        | 4        | Dairy Flat ↔ Great Barrier (NZGB)    | MWF outbound, TTS return           |
| HondaJet Elite     | 5        | Dairy Flat ↔ Tuuta (NZCI)            | Tue/Fri outbound, Wed/Sat return   |
| HondaJet Elite     | 5        | Dairy Flat ↔ Lake Tekapo (NZTL)      | Mon outbound, Tue return           |

Timezones handled:
- **NZ Mainland (NZNE)** – GMT+12
- **Chatham Islands (NZCI)** – GMT+12:45
- **Melbourne (YMML)** – GMT+10

---

## 🧱 Technologies Used

- **Python 3.x**
- **Flask** (backend web framework)
- **SQLite** (lightweight database)
- **Jinja2** (templating engine for HTML rendering)
- **Bootstrap 5** (frontend styling)
- **Datetime/timezone modules** for flight time accuracy

---

## ⚙️ Build & Run Instructions (via PyCharm)

Open the project in PyCharm
Set up a Python interpreter and install dependencies:
```bash
pip install -r requirements.txt
pip install django
python manage.py migrate
python manage.py runserver
```
Visit -- http://127.0.0.1:8000/
