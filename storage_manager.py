import sqlite3
import json
import pandas as pd

def store_use_case(data, db_path='use_cases.db'):
    """
    Store the use case data into an SQLite database.
    If using a DataFrame, we assume each row represents a use case.
    """
    conn = sqlite3.connect(db_path)
    # For dictionary input, convert to DataFrame first
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise TypeError("Data must be a dict or DataFrame.")
    
    df.to_sql('use_cases', conn, if_exists='append', index=False)
    conn.close()

def search_use_cases(query, db_path='use_cases.db'):
    """
    Search stored use cases by a query string.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM use_cases WHERE use_case LIKE '%{query}%'", conn)
    conn.close()
    return df

def export_use_cases_to_json(db_path='use_cases.db', json_path='use_cases.json'):
    """
    Export all stored use cases to a JSON file.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM use_cases", conn)
    conn.close()
    df.to_json(json_path, orient='records', indent=4)
