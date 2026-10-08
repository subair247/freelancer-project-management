import pymysql
import pymysql.cursors
from config.db_config import get_db_connection

def add_project(client_id, project_name, milestones, deadline, project_status):
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed!"
    
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO projects (client_id, project_name, milestones, deadline, project_status) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (client_id, project_name, milestones, deadline, project_status))
        connection.commit()
        return True, "Project added successfully!"
    except Exception as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

def get_projects(user_id):
    connection = get_db_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
            SELECT p.*, c.client_name FROM projects p
            JOIN clients c ON p.client_id = c.client_id
            WHERE c.user_id = %s
        """
        cursor.execute(query, (user_id,))
        projects = cursor.fetchall()
        return projects
    except Exception as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()