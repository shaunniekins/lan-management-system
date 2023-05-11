import mysql.connector


def get_database():
    db = mysql.connector.connect(
        host="localhost",  # server: ip address
        user="joel",
        password="Hello_World123",
        database="lan_management_system"
    )
    return db
