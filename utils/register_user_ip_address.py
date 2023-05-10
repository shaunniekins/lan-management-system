import socket
from utils.db_connection import get_database


def check_user_ip_address(user_id, user_type, ip_address, is_active):
    db = get_database()
    cursor = db.cursor()

    query = f"SELECT * FROM active_user_ip WHERE user_id = '{user_id}' AND user_type = '{user_type}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        query = "UPDATE active_user_ip SET ip_address=%s, is_active=%s WHERE user_id=%s;"
        values = (ip_address, is_active, user_id)
        cursor.execute(query, values)
        result = cursor.fetchone()
    else:
        query = "INSERT INTO active_user_ip(user_id, user_type, ip_address, is_active) VALUES (%s, %s, %s, %s)"
        values = (user_id, user_type, ip_address, is_active)
        cursor.execute(query, values)
        result = cursor.fetchone()

    db.commit()
    cursor.close()
    db.close()


def close_lan_active(user_id, is_active):
    db = get_database()
    cursor = db.cursor()
    query = "UPDATE active_user_ip SET is_active=%s WHERE user_id=%s;"
    values = (is_active, user_id)
    cursor.execute(query, values)

    db.commit()
    cursor.close()
    db.close()
