import mysql.connector


def get_database():
    db = mysql.connector.connect(
        host="192.168.0.115",  # server: ip address
        user="joel",
        password="Hello_World123",
        database="lan_management_system"
    )
    return db
