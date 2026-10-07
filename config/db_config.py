import os
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Returns a MySQL database connection supporting both:
    1. Local XAMPP (using .env variables)
    2. Streamlit Cloud / Production (using st.secrets & TiDB Cloud with SSL)
    """
    try:
        if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
            connection = mysql.connector.connect(
                host=st.secrets["DB_HOST"],
                port=int(st.secrets.get("DB_PORT", 4000)),
                user=st.secrets["DB_USER"],
                password=st.secrets["DB_PASSWORD"],
                database=st.secrets["DB_NAME"],
                ssl_verify_cert=True
            )
        else:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "freelancing_db")
            )
        return connection
    except mysql.connector.Error as err:
        if hasattr(st, "error"):
            st.error(f"Database connection error: {err}")
        else:
            print(f"Database connection error: {err}")
        return None