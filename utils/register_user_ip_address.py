import socket
from utils.db_connection import get_database

def check_user_ip_address(user_id, user_type, ip_address, is_active):
    db = get_database()
    cursor = db.cursor()

    try:
        # Check if the IP address exists for the user
        query = "SELECT * FROM active_user_ip WHERE user_id = %s AND user_type = %s"
        values = (user_id, user_type)
        cursor.execute(query, values)
        result = cursor.fetchall()

        if result:
            # Update the existing IP address
            query = "UPDATE active_user_ip SET ip_address = %s, is_active = %s WHERE user_id = %s AND user_type = %s"
            values = (ip_address, is_active, user_id, user_type)
            cursor.execute(query, values)
            db.commit()
        else:
            # Insert a new IP address
            query = "INSERT INTO active_user_ip (user_id, user_type, ip_address, is_active) VALUES (%s, %s, %s, %s)"
            values = (user_id, user_type, ip_address, is_active)
            cursor.execute(query, values)
            db.commit()
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()


def check_user_ip_address_student(user_id, user_type, ip_address, connection_ip_address, is_active):
    db = get_database()
    cursor = db.cursor()

    try:
        query = f"SELECT * FROM active_user_ip WHERE user_id = '{user_id}' AND user_type = '{user_type}'"
        cursor.execute(query)
        cursor.fetchall()  # Clear any unread results

        if cursor.rowcount > 0:
            query = "UPDATE active_user_ip SET ip_address=%s, is_active=%s, connection_ip_address=%s WHERE user_id=%s;"
            values = (ip_address, is_active, connection_ip_address, user_id)
            cursor.execute(query, values)
        else:
            query = "INSERT INTO active_user_ip(user_id, user_type, ip_address, connection_ip_address, is_active) VALUES (%s, %s, %s, %s, %s)"
            values = (user_id, user_type, ip_address, connection_ip_address, is_active)
            cursor.execute(query, values)

        db.commit()
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()
        

def close_lan_active(user_id, is_active):
    db = get_database()
    cursor = db.cursor()

    try:
        query = "UPDATE active_user_ip SET is_active=%s WHERE user_id=%s;"
        values = (is_active, user_id)
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        db.rollback
    finally:
        cursor.close()
        db.close()

def close_lan_active_student(user_id, is_active, connection_ip_address):
    db = get_database()
    cursor = db.cursor()

    try:
        query = "UPDATE active_user_ip SET is_active=%s, connection_ip_address=%s WHERE user_id=%s AND user_type = 'student';"
        values = (is_active, connection_ip_address, user_id)
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

