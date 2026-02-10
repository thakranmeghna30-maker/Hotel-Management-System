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
