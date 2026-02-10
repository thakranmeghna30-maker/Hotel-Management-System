#  Hotel Management System (Python + MySQL)

A **menu-driven Hotel Management System** built using **Python** and **MySQL** to manage hotel operations such as guest records, room allocation, reservations, billing, and revenue tracking.

The system supports both **online (advance)** and **offline (walk-in)** bookings with automatic room availability management.

---

##  Features

###  Guest Management
- Add, view, search, update, and delete guest records
- Store guest contact details and number of people staying

###  Room Management
- Add and delete rooms
- Store room type and price per night
- Track and display available rooms automatically

###  Reservation Management
- Offline room assignment for walk-in guests
- Online/advance reservations before arrival
- Automatic guest registration if not already present
- Room selection based on availability and room type
- Modify reservation dates
- Cancel reservations and free rooms automatically

###  Billing & Revenue
- Generate guest bills based on:
  - Room price
  - Duration of stay
  - Number of people
- Calculate total hotel revenue from completed stays

###  System Highlights
- Menu-driven interface
- Proper database relationships using foreign keys
- Buffered cursor to prevent unread result errors
- Modular and well-structured code

---

##  Technologies Used
- Python 3
- MySQL
- mysql-connector-python
- datetime module

---

##  Database Structure
- **Guests** – Guest personal details
- **Rooms** – Room information and availability
- **Reservations** – Guest-room mapping with stay duration

---

##  How to Run

1. Create database:
   ```sql
   CREATE DATABASE hotel_management;
2. Install dependency:
   pip install mysql-connector-python
3. Update database credentials in the code.
4. Run the program:
   python hotel_management.py

---

##  Learning Outcomes
- Python–MySQL integration
- Database design and CRUD operations
- Real-world reservation and billing logic
- Modular programming

---

##  Author
Meghna Thakran

Beginner in Machine Learning & Python

   
