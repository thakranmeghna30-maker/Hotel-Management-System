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
