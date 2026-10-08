import os
import pymysql
import streamlit as st
import certifi
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Returns a MySQL database connection using PyMySQL supporting both:
    1. Local XAMPP (using .env variables)
    2. Streamlit Cloud / TiDB Cloud (using st.secrets, certifi SSL)
    """
    try:
        if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
            db_user = st.secrets.get("DB_USER") or st.secrets.get("DB_USERNAME")
            db_name = st.secrets.get("DB_NAME") or st.secrets.get("DB_DATABASE")
            
            connection = pymysql.connect(
                host=st.secrets["DB_HOST"],
                port=int(st.secrets.get("DB_PORT", 4000)),
                user=db_user,
                password=st.secrets["DB_PASSWORD"],
                database=db_name,
                ssl={'ca': certifi.where()}
            )
        else:
            connection = pymysql.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "freelancing_db")
            )
        return connection
    except Exception as err:
        if hasattr(st, "error"):
            st.error(f"Database connection error: {err}")
        else:
            print(f"Database connection error: {err}")
        return None