import csv
from datetime import datetime,timedelta
from raise_error import application_error
from windows_notification11 import windows_not
# Get the current date and time
date = datetime.now()
# Define the new values
# cardId = 'TN04A59722'

# Define the CSV file path
csv_file_path = r'D:\working_directory\AnprApiService\test_windowsLog_0.1\datatest.csv'

def read_csv(cardId):
    # Check if the CSV file exists and has data
    try:
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            print(rows)

            # Check if the file contains data and if the values are different
            if rows and len(rows[0]) == 2 and rows[0][1] == cardId:
                print("Values are the same. Not saving to the file.")

                stored_date_str = rows[0][0]
                stored_date = datetime.strptime(stored_date_str, "%Y-%m-%d %H:%M:%S.%f")

                current_date = datetime.now()

                # Check if the stored date is more than 24 hours old
                print('current_date - stored_date',current_date - stored_date,current_date,stored_date)
                if (current_date - stored_date) >= timedelta(hours=24):
                    print("Stored date is more than 24 hours old.")
                    application_error("Stored date is more than 24 hours old.")
                    windows_not('Anpr',f"Stored date is more than 24 hours old. last dated on {stored_date} for vehcle {str(rows[0][1])}")

                else:
                    print("Stored date is within 24 hours.")
                    return True
            else:
                # Values are different or the file is empty, so write the new values
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([date, cardId])
                    print("Values saved to the file.")
                    return None
    except FileNotFoundError:
        # If the file doesn't exist, write the new values
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, cardId])
            print("Values saved to the file.")

#print(read_csv(cardId))
