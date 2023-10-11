import mysql.connector
from datetime import datetime, timedelta
# MySQL server connection parameters


db_config = {}
with open('db_config.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        db_config[key.strip()] = value.strip()

host=db_config['host']
username=db_config['user']
password=db_config['password']
database=db_config['database']



def GetPrevTransactionDetails(sql_query):
    try:
        # MySQL connection settings
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        # Connect to the MySQL database

        cursor = conn.cursor()

        cursor.execute(sql_query)

        # Fetch the data
        data = cursor.fetchone()

        # Create a dictionary where column names are keys and data values are values
        result_dict = {}
        if data:
            for column_name, value in zip(cursor.column_names, data):
                result_dict[column_name] = value

        conn.close()
        return result_dict
    except Exception as e:
        return {'error':str(e)}