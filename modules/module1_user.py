import hashlib
import pymysql
import pymysql.cursors
from config.db_config import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, skills):
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed!"
    
    cursor = connection.cursor()
    password_hash = hash_password(password)
    
    try:
        query = "INSERT INTO users (username, email, password_hash, skills) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, email, password_hash, skills))
        connection.commit()
        return True, "Registration successful!"
    except Exception as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

def login_user(email, password):
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed!"
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    password_hash = hash_password(password)
    
    try:
        query = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        cursor.execute(query, (email, password_hash))
        user = cursor.fetchone()
        if user:
            return True, user
        else:
            return False, "Invalid email or password."
    except Exception as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        connection.close()