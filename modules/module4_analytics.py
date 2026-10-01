import mysql.connector
from config.db_config import get_db_connection

def add_performance_log(project_id, income_generated, feedback_score, improvisation_notes):
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed!"
    
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO performance_logs (project_id, income_generated, feedback_score, improvisation_notes) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (project_id, income_generated, feedback_score, improvisation_notes))
        connection.commit()
        return True, "Analytics and performance logged successfully!"
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

def get_performance_logs(user_id):
    connection = get_db_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT pl.*, p.project_name, c.client_name FROM performance_logs pl
            JOIN projects p ON pl.project_id = p.project_id
            JOIN clients c ON p.client_id = c.client_id
            WHERE c.user_id = %s
        """
        cursor.execute(query, (user_id,))
        logs = cursor.fetchall()
        return logs
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()