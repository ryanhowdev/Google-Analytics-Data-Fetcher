# README for Google Analytics Data Fetcher

## Overview

The Google Analytics Data Fetcher is a Python application designed to retrieve data from a specified Google Analytics account over a given time period and save it in either a CSV, JSON file format, or directly into a MySQL, PostgreSQL, or SQLite database. This application utilizes the Google Analytics API to fetch analytics data, providing users with a flexible way to access and store their data.

## Prerequisites

Before running this application, ensure you have:
- Python 3.6 or higher installed on your machine.
- Access to a Google Analytics account with the necessary permissions to view and retrieve analytics data.

## Installation

1. **Clone the Repository:**
   Clone this repository to your local machine using `git clone`, followed by the repository URL.

2. **Install Required Python Libraries:**
   Open a terminal and navigate to the project directory. Install the required libraries using pip:

   ```bash
   pip install --upgrade google-api-python-client oauth2client mysql-connector-python psycopg2
   ```

3. **Google Cloud Project Setup:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Google Analytics API for your project.
   - Create credentials for a Service Account and download the JSON key file.

## Configuration

- **Service Account JSON Key File:** Place your downloaded Service Account JSON key file in a secure and accessible location on your machine.
- **Modify the Script:** Open the `google_analytics_data_fetcher.py` script in your favorite text editor or IDE. Update the `KEY_FILE_PATH` and `VIEW_ID` constants with the path to your Service Account JSON key file and your Google Analytics View ID, respectively.

## Usage

1. **Running the Application:**
   Open a terminal, navigate to the project directory, and run the script:

   ```bash
   python google_analytics_data_fetcher.py
   ```

2. **Follow the On-screen Prompts:**
   - The application will first ask whether you want to save the data to a file or a database. Enter `F` for file or `D` for database.
   - If you choose file (`F`), specify the desired file format (`CSV` or `JSON`) and the path where you want to save the file.
   - If you choose database (`D`), specify the database type (`sqlite`, `mysql`, `postgresql`), and then enter the required database credentials as prompted.

## Methods

- **`initialize_analyticsreporting()`:** Initializes the Analytics Reporting API V4 service object.
- **`get_report(analytics, start_date, end_date)`:** Queries the Analytics Reporting API V4 with the specified parameters.
- **`save_response_to_file(response, file_format, file_path)`:** Saves the API response to a file in either CSV or JSON format.
- **`save_response_to_db(response, db_type, db_credentials)`:** Saves the API response to a specified database. Supports SQLite, MySQL, and PostgreSQL.

## External References

- **Google Analytics API:** For detailed information about the Google Analytics API, visit the [official documentation](https://developers.google.com/analytics/devguides/reporting/core/v4/).
- **Google API Python Client:** Learn more about using the Google API Python Client [here](https://github.com/googleapis/google-api-python-client).
- **OAuth2Client:** Additional details on OAuth2Client can be found [here](https://oauth2client.readthedocs.io/en/latest/).

## Additional Notes

- Ensure your Google Cloud project and Analytics account have the necessary permissions set to use the API.
- The database saving functionality requires that the user has the necessary permissions to create tables and insert data into the specified database.
- This application is meant for educational and demonstration purposes. Adjust security and error handling as necessary for production environments.

By following these instructions and utilizing the provided methods, you can efficiently fetch and store Google Analytics data using this Python application.