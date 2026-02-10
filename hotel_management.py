import mysql.connector
from datetime import datetime

# -------------------- DATABASE CONNECTION --------------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Meghna@mysql",
    database="hotel_management"
)
cursor = connection.cursor(buffered=True)

# -------------------- TABLE CREATION --------------------
def create_tables():
    # Guests table stores personal details of guests
    create_guests_table = """
    CREATE TABLE IF NOT EXISTS guests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(255),
        num_people INT
    );
    """
    cursor.execute(create_guests_table)

    # Rooms table stores room details and availability
    create_rooms_table = """
    CREATE TABLE IF NOT EXISTS rooms (
        id INT AUTO_INCREMENT PRIMARY KEY,
        room_number VARCHAR(20) UNIQUE NOT NULL,
        room_type VARCHAR(50),
        price DECIMAL(10, 2),
        available BOOLEAN DEFAULT TRUE
    );
    """
    cursor.execute(create_rooms_table)

    # Reservations table links guests and rooms
    create_reservations_table = """
    CREATE TABLE IF NOT EXISTS reservations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        guest_id INT,
        room_number VARCHAR(20),
        check_in_date DATE,
        check_out_date DATE,
        FOREIGN KEY (guest_id) REFERENCES guests(id),
        FOREIGN KEY (room_number) REFERENCES rooms(room_number)
    );
    """
    cursor.execute(create_reservations_table)

    connection.commit()
    print("Tables created successfully!")
    print("-" * 160)

create_tables()

# -------------------- GUEST MANAGEMENT --------------------
def add_guest():
    name = input("Enter guest name: ")
    contact = input("Enter guest contact: ")
    email = input("Enter guest email: ")
    num_people = int(input("Enter number of people staying: "))

    cursor.execute(
        "INSERT INTO guests (name, contact, email, num_people) VALUES (%s, %s, %s, %s)",
        (name, contact, email, num_people)
    )
    connection.commit()
    print("Guest added successfully!")
    print("-" * 160)

def view_guests():
    cursor.execute("SELECT * FROM guests")
    for guest in cursor.fetchall():
        print(guest)
    print("-" * 160)

def search_guest():
    guest_id = input("Enter guest ID to search: ")
    cursor.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
    guest = cursor.fetchone()

    if guest:
        print(guest)
    else:
        print("Guest not found.")
    print("-" * 160)

def update_guest():
    # Allows partial update of guest details
    guest_id = input("Enter guest ID to update: ")
    print("Press Enter to skip any field")

    name = input("Enter new name: ")
    contact = input("Enter new contact: ")
    email = input("Enter new email: ")
    num_people = input("Enter new number of people staying: ")

    if name:
        cursor.execute("UPDATE guests SET name = %s WHERE id = %s", (name, guest_id))
    if contact:
        cursor.execute("UPDATE guests SET contact = %s WHERE id = %s", (contact, guest_id))
    if email:
        cursor.execute("UPDATE guests SET email = %s WHERE id = %s", (email, guest_id))
    if num_people:
        cursor.execute("UPDATE guests SET num_people = %s WHERE id = %s", (num_people, guest_id))

    connection.commit()
    print("Guest updated successfully!")
    print("-" * 160)

def delete_guest():
    guest_id = input("Enter guest ID to delete: ")
    cursor.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
    connection.commit()
    print("Guest deleted successfully!")
    print("-" * 160)

    # -------------------- ROOM MANAGEMENT --------------------
def add_room():
    room_number = input("Enter room number: ")
    room_type = input("Enter room type: ")
    price = float(input("Enter price per night: "))

    cursor.execute(
        "INSERT INTO rooms (room_number, room_type, price, available) VALUES (%s, %s, %s, %s)",
        (room_number, room_type, price, True)
    )
    connection.commit()
    print("Room added successfully!")
    print("-" * 160)

def delete_room():
    # Ensures room exists before deleting
    room_number = input("Enter room number to delete: ")

    cursor.execute("SELECT * FROM rooms WHERE room_number = %s", (room_number,))
    if not cursor.fetchone():
        print("Room number not found.")
        return

    cursor.execute("DELETE FROM rooms WHERE room_number = %s", (room_number,))
    connection.commit()
    print(f"Room {room_number} deleted successfully!")

def list_available_rooms():
    cursor.execute("SELECT * FROM rooms WHERE available = TRUE")
    for room in cursor.fetchall():
        print(room)
    print("-" * 160)

# -------------------- RESERVATION MANAGEMENT --------------------
def assign_room():
    # Assigns a room directly at the hotel (offline booking)
    guest_id = input("Enter guest ID: ")

    cursor.execute(
        """SELECT id FROM reservations
           WHERE guest_id = %s
           AND check_in_date <= CURDATE()
           AND check_out_date >= CURDATE()""",
        (guest_id,)
    )

    if cursor.fetchone():
        print("Guest already has a reservation.")
        return

    cursor.execute("SELECT room_number FROM rooms WHERE available = TRUE LIMIT 1")
    room = cursor.fetchone()

    if room:
        room_number = room[0]
        cursor.execute("UPDATE rooms SET available = FALSE WHERE room_number = %s", (room_number,))
        cursor.execute(
            "INSERT INTO reservations (guest_id, room_number, check_in_date, check_out_date) VALUES (%s, %s, CURDATE(), NULL)",
            (guest_id, room_number)
        )
        connection.commit()
        print("Room assigned successfully!")
    else:
        print("No rooms available.")

    print("-" * 160)

def make_reservation():
    # Online / advance reservation before arrival
    print("Online Reservation System")

    guest_name = input("Enter your full name: ")
    contact = input("Enter your contact number: ")
    email = input("Enter your email address: ")
    num_people = int(input("Enter the number of people: "))

    cursor.execute("SELECT id FROM guests WHERE name = %s AND contact = %s", (guest_name, contact))
    guest = cursor.fetchone()

    if guest:
        guest_id = guest[0]
    else:
        cursor.execute(
            "INSERT INTO guests (name, contact, email, num_people) VALUES (%s, %s, %s, %s)",
            (guest_name, contact, email, num_people)
        )
        connection.commit()
        guest_id = cursor.lastrowid

    cursor.execute("SELECT DISTINCT room_type FROM rooms WHERE available = TRUE")
    room_types = cursor.fetchall()

    for i, r in enumerate(room_types, 1):
        print(f"{i}. {r[0]}")

    selected_room_type = room_types[int(input("Select room type: ")) - 1][0]

    cursor.execute(
        "SELECT room_number FROM rooms WHERE room_type = %s AND available = TRUE",
        (selected_room_type,)
    )
    room = cursor.fetchone()

    if not room:
        print("No room available.")
        return

    check_in = input("Enter check-in date (YYYY-MM-DD): ")
    check_out = input("Enter check-out date (YYYY-MM-DD): ")

    datetime.strptime(check_in, "%Y-%m-%d")
    datetime.strptime(check_out, "%Y-%m-%d")

    cursor.execute(
        "INSERT INTO reservations (guest_id, room_number, check_in_date, check_out_date) VALUES (%s, %s, %s, %s)",
        (guest_id, room[0], check_in, check_out)
    )
    cursor.execute("UPDATE rooms SET available = FALSE WHERE room_number = %s", (room[0],))
    connection.commit()

    print("Reservation successful!")

def cancel_reservation():
    # Cancels an existing reservation and frees the room
    reservation_id = input("Enter reservation ID to cancel: ")

    cursor.execute(
        "SELECT room_number FROM reservations WHERE id = %s",
        (reservation_id,)
    )
    reservation = cursor.fetchone()

    if reservation:
        room_number = reservation[0]

        cursor.execute(
            "DELETE FROM reservations WHERE id = %s",
            (reservation_id,)
        )
        cursor.execute(
            "UPDATE rooms SET available = TRUE WHERE room_number = %s",
            (room_number,)
        )

        connection.commit()
        print("Reservation cancelled successfully!")
    else:
        print("Invalid reservation ID.")

    print("-" * 160)

def modify_reservation():
    # Allows changing check-in or check-out date of an existing reservation
    reservation_id = input("Enter reservation ID to modify: ")
    print("Press Enter to skip any field")

    check_in_date = input("Enter new check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter new check-out date (YYYY-MM-DD): ")

    if check_in_date:
        cursor.execute(
            "UPDATE reservations SET check_in_date = %s WHERE id = %s",
            (check_in_date, reservation_id)
        )

    if check_out_date:
        cursor.execute(
            "UPDATE reservations SET check_out_date = %s WHERE id = %s",
            (check_out_date, reservation_id)
        )

    connection.commit()
    print("Reservation modified successfully!")
    print("-" * 160)

# -------------------- BILLING & FINANCE --------------------
def generate_bill():
    # Calculates bill based on stay duration and room price
    guest_id = input("Enter guest ID to generate bill: ")
    if not guest_id.isdigit():
        print("Invalid guest ID.")
        return

    cursor.execute("""
        SELECT rooms.price,
               DATEDIFF(reservations.check_out_date, reservations.check_in_date),
               guests.num_people
        FROM reservations
        INNER JOIN rooms ON reservations.room_number = rooms.room_number
        INNER JOIN guests ON reservations.guest_id = guests.id
        WHERE reservations.guest_id = %s
        AND reservations.check_out_date IS NOT NULL;
    """, (guest_id,))

    total = 0
    for price, days, people in cursor.fetchall():
        total += price * days * people

    print(f"Total Bill: ${total:.2f}")

def calculate_revenue():
    # Calculates total hotel revenue
    cursor.execute("""
        SELECT rooms.price,
               DATEDIFF(reservations.check_out_date, reservations.check_in_date),
               guests.num_people
        FROM reservations
        INNER JOIN rooms ON reservations.room_number = rooms.room_number
        INNER JOIN guests ON reservations.guest_id = guests.id
        WHERE reservations.check_out_date IS NOT NULL;
    """)

    revenue = 0
    for price, days, people in cursor.fetchall():
        revenue += price * days * people

    print(f"Total Revenue: ${revenue:.2f}")

# -------------------- MAIN MENU --------------------
def main():
    while True:
        print("\nHotel Management System")
        print("1. Room Management")
        print("2. Reservation Management")
        print("3. Guest Management")
        print("4. Billing and Finance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '3':
            print("\nGuest Management")
            print("1. Add Guest")
            print("2. View Guests")
            print("3. Search Guest")
            print("4. Update Guest")
            print("5. Delete Guest")

            g = input("Enter your choice: ")
            if g == '1': add_guest()
            elif g == '2': view_guests()
            elif g == '3': search_guest()
            elif g == '4': update_guest()
            elif g == '5': delete_guest()

        elif choice == '1':
            print("\nRoom Management")
            print("1. Add Room")
            print("2. Delete Room")
            print("3. List Rooms")

            r = input("Enter your choice: ")
            if r == '1': add_room()
            elif r == '2': delete_room()
            elif r == '3': list_available_rooms()

        elif choice == '2':
            print("\nReservation Management")
            print("1. Assign Room")
            print("2. Make Reservation")
            print("3. Cancel Reservation")
            print("4. Modify Reservation")

            r = input("Enter your choice: ")
            if r == '1': assign_room()
            elif r == '2': make_reservation()
            elif r == '3': cancel_reservation()
            elif r == '4': modify_reservation()

        elif choice == '4':
            print("\nBilling and Finance")
            print("1. Generate Bill")
            print("2. Calculate Revenue")

            b = input("Enter your choice: ")
            if b == '1': generate_bill()
            elif b == '2': calculate_revenue()

        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid choice!")

main()
cursor.close()
connection.close()

