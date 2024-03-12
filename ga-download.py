import os
import sqlite3
import mysql.connector
import psycopg2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import json
import csv
import sys

# Environment variables for sensitive information
KEY_FILE_PATH = os.getenv('GA_KEY_FILE_PATH')
VIEW_ID = os.getenv('GA_VIEW_ID')
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object with error handling."""
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_PATH, SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        return analytics
    except FileNotFoundError:
        print("The service account JSON key file was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during Analytics Reporting API service initialization: {e}")
        sys.exit(1)

def get_report(analytics, start_date, end_date):
    """Queries the Analytics Reporting API V4 with error handling."""
    try:
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'metrics': [{'expression': 'ga:sessions'}],
                        'dimensions': [{'name': 'ga:country'}]
                    }]
            }
        ).execute()
    except HttpError as error:
        print(f"An HTTP error occurred: {error.resp.status} {error.error_details}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while querying the Analytics Reporting API: {e}")
        sys.exit(1)

def save_response_to_file(response, file_format, file_path):
    """Saves the API response to a file with error handling."""
    try:
        if file_format.lower() == 'json':
            with open(file_path, 'w') as jsonfile:
                json.dump(response, jsonfile, indent=2)
        elif file_format.lower() == 'csv':
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Country', 'Sessions'])  # Column headers
                for report in response.get('reports', []):
                    rows = report.get('data', {}).get('rows', [])
                    for row in rows:
                        dimensions = row.get('dimensions', [])
                        metrics = row.get('metrics', [])[0].get('values', [])
                        writer.writerow(dimensions + metrics)
        else:
            print("Unsupported file format. Please choose either CSV or JSON.")
    except IOError as e:
        print(f"An error occurred while writing to file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def connect_to_database(db_type, db_credentials):
    """Establishes database connection with error handling."""
    try:
        if db_type == 'sqlite':
            conn = sqlite3.connect(db_credentials['db_name'])
        elif db_type == 'mysql':
            conn = mysql.connector.connect(
                host=db_credentials['host'],
                user=db_credentials['user'],
                password=db_credentials['password'],
                database=db_credentials['db_name'],
                use_pure=True  # Use the pure Python implementation
            )
        elif db_type == 'postgresql':
            conn = psycopg2.connect(
                host=db_credentials['host'],
                database=db_credentials['db_name'],
                user=db_credentials['user'],
                password=db_credentials['password']
            )
        else:
            print("Unsupported database type. Supported types are: sqlite, mysql, postgresql.")
            sys.exit(1)
        return conn
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        sys.exit(1)

def save_response_to_db(response, db_type, db_credentials):
    """Saves the response data to the specified database with error handling."""
    conn = connect_to_database(db_type, db_credentials)
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS analytics_data (country VARCHAR(255), sessions INT)")
        data = []
        for report in response.get('reports', []):
            rows = report.get('data', {}).get('rows', [])
            for row in rows:
                country = row.get('dimensions', [])[0]
                sessions = row.get('metrics', [])[0].get('values', [])[0]
                data.append((country, sessions))
        insert_query = "INSERT INTO analytics_data (country, sessions) VALUES (%s, %s)"
        cur.executemany(insert_query, data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred while inserting data into the database: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    analytics = initialize_analyticsreporting()
    start_date = '2023-01-01'
    end_date = '2023-01-31'
    response = get_report(analytics, start_date, end_date)

    save_option = input("Do you want to save data to a file (F) or database (D)? ").lower()
    if save_option == 'f':
        file_format = input("Enter the file format (CSV/JSON): ")
        file_path = input("Enter the file path to save the data: ")
        save_response_to_file(response, file_format, file_path)
        print(f"Data saved to {file_path} in {file_format} format.")
    elif save_option == 'd':
        db_type = input("Enter the database type (sqlite, mysql, postgresql): ").lower()
        db_credentials = {}
        if db_type in ['mysql', 'postgresql']:
            db_credentials['host'] = input("Enter the database host: ")
            db_credentials['user'] = input("Enter the database user: ")
            db_credentials['password'] = input("Enter the database password: ")
            db_credentials['db_name'] = input("Enter the database name: ")
        elif db_type == 'sqlite':
            db_credentials['db_name'] = input("Enter the SQLite database file path: ")
        else:
            print("Unsupported database type")
        save_response_to_db(response, db_type, db_credentials)
