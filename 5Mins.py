import time
import requests
import csv
from datetime import datetime,timedelta
#from raise_error import application_error
#from windows_notification11 import windows_not
# from plyer import notification
import win32evtlog

# Get the current date and time
date = datetime.now()



def application_error(message):
    # Log the exception to the Windows Event Log
    log_type = 'iParkANPR'  # You can change this to 'Security', 'System', etc.
    event_id = 1005  # You can choose a unique event ID
    event_category = 0  # The category of the event (0 for none)
    description = "Please restart your device . New Data Not Comming."
    event_strings = [f"Exception occurred: {message}",description]

    # # Additional information for the event

    # task_category = 1  # You can choose an appropriate task category

    # Open the event log for writing
    h_log = win32evtlog.OpenEventLog(None, log_type)

    # Print parameters for debugging
    #print(f"log_type: {log_type}, event_id: {event_id}, event_category: {event_category}, event_strings: {event_strings}")

    # Report the event
    win32evtlog.ReportEvent(
        h_log,
        win32evtlog.EVENTLOG_ERROR_TYPE,
        event_category,
        event_id,
        None,
        event_strings,
        None,

    )

    # Close the event log
    win32evtlog.CloseEventLog(h_log)
    return message



#
# # Notification title and message
# # title = 'My Notification'
# # message = 'This is a sample notification.'
#



# def windows_not(title,message):
#     # Send the notification
#     notification.notify(
#     title=title,
#     message=message,
#     app_name='Anpr',  # Set your app name
#     timeout=40  # Notification display time in seconds
# )


#
#
# csv_file_path = r'datatest.csv'
#
# def read_csv(cardId):
#     # Check if the CSV file exists and has data
#     try:
#         with open(csv_file_path, mode='r', newline='') as file:
#             reader = csv.reader(file)
#             rows = list(reader)
#             #print(rows)
#
#             # Check if the file contains data and if the values are different
#             if rows and len(rows[0]) == 2 and rows[0][1] == cardId:
#                 #print("Values are the same. Not saving to the file.")
#
#                 stored_date_str = rows[0][0]
#                 stored_date = datetime.strptime(stored_date_str, "%Y-%m-%d %H:%M:%S.%f")
#
#                 current_date = datetime.now()
#
#                 # Check if the stored date is more than 24 hours old
#                 #print('current_date - stored_date',current_date - stored_date,current_date,stored_date)
#                 if (current_date - stored_date) >= timedelta(hours=24):
#                     #print("Stored date is more than 24 hours old.")
#                     application_error(f"Stored date is more than 24 hours old. last dated on {stored_date} for vehcle {str(rows[0][1])}")
#                     windows_not('Anpr',f"Stored date is more than 24 hours old. last dated on {stored_date} for vehcle {str(rows[0][1])}")
#
#                 else:
#                     #print("Stored date is within 24 hours.")
#                     return True
#             else:
#                 # Values are different or the file is empty, so write the new values
#                 with open(csv_file_path, mode='w', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow([date, cardId])
#                     #print("Values saved to the file.")
#                     return None
#     except FileNotFoundError:
#         # If the file doesn't exist, write the new values
#         with open(csv_file_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([date, cardId])
#             #print("Values saved to the file.")

def read_data_from_file():
    data = {}

    # Open the file for reading
    with open('UrlAndPaths.txt', 'r') as file:
        for line in file:
            # Split each line into key and value pairs
            key, value = line.strip().split('=')
            # Remove leading and trailing spaces from key and value
            key = key.strip()
            value = value.strip()
            # Store the data in a dictionary
            data[key] = value

    return data

end_time = datetime.now() + timedelta(days=30)

while datetime.now() < end_time:
    #print("Running your task at:", datetime.now())

    try:

        txt_data = read_data_from_file()
        if 'url' in txt_data:
            url = txt_data['url']
        if 'path' in txt_data:
            path = txt_data['path']

        # url = 'http://192.168.4.70:8020/api/vehicle/getprevtransaction'
        #url = 'http://192.168.1.18:3333/api/vehicle/getprevtransaction'
        response = requests.get(url)
        data = response.json()
        data['vehicleImage'] = ''
        data['numberPlateImage'] = ''
        data['numberPlateImageb64'] = ''
        data['vehicleImageb64'] = ''

        with open(path, 'a') as file:
            file.write(f" {str(datetime.now())} :  {data}    " + '\n' + '----------------------------------------------------------------------' + '\n')

        ## read_csv(data['cardId'])

        cardId = data['cardId']
        dateOfTransaction = data['dateOfTransaction']
        # Convert the string to a datetime object
        dt1 = datetime.fromisoformat(dateOfTransaction)

        # Get the current time as a datetime object
        current_time = datetime.now()

        # Calculate the difference in hours
        time_difference = (current_time - dt1).total_seconds() / 3600

        if time_difference > 22:

            application_error(f"Stored date is more than 24 hours old. last dated on {dateOfTransaction} for vehcle {cardId}")
            # windows_not('Anpr',f"Stored date is more than 24 hours old. last dated on {dateOfTransaction} for vehcle {cardId}")

            with open(path, 'a') as file:
                file.write(
                    f" {str(datetime.now())} :  error raised in event viewer    " + '\n' + '----------------------------------------------------------------------' + '\n')


    except requests.exceptions.RequestException as e:
        with open(path, 'a') as file:
            file.write(f" {str(datetime.now())} : Error :  {e}    " + '\n' + '----------------------------------------------------------------------' + '\n')

    # Wait for 5 minutes
    time.sleep(300)  # 5 minutes in seconds
