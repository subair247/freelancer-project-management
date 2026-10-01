import mysql.connector
from config.db_config import get_db_connection

def add_client(user_id, client_name, company_name, contact_email, status):
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed!"
    
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO clients (user_id, client_name, company_name, contact_email, status) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, client_name, company_name, contact_email, status))
        connection.commit()
        return True, "Client added successfully!"
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

def get_clients(user_id):
    connection = get_db_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM clients WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        clients = cursor.fetchall()
        return clients
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()