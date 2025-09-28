import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    """
    Returns a dictionary with configuration settings.
    Replace the default values with your actual database credentials and API key.
    It's recommended to use environment variables for sensitive data.
    """
    return {
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_host": os.getenv("DB_HOST"),
        "db_name": os.getenv("DB_NAME"),
        "gemini_api_key": os.getenv("GEMINI_API_KEY")
    }