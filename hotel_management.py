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
