import mysql.connector
import requests
import base64

db_config = {}
with open('db_config.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        db_config[key.strip()] = value.strip()
host=db_config['host']
username=db_config['user']
password=db_config['password']
database=db_config['database']

def db_update_record(sql_query):
    try:
        # MySQL connection settings
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        cursor = conn.cursor()

        cursor.execute(sql_query)
        conn.commit()  # Commit the changes to the database

        conn.close()
        return "Record updated successfully.", 200
    except mysql.connector.Error as e:
        return {'error': str(e)}, 400  # Handle database errors
    except Exception as e:
        return {'error': str(e)}, 500  # Handle other exceptions

def dbgetlasttransactions(sql_query):
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

        # Fetch all the data
        data = cursor.fetchall()

        if not data:
            return []

        # Create a list of dictionaries, where each dictionary represents a record
        result_list = []
        for row in data:
            result_dict = {}
            for column_name, value in zip(cursor.column_names, row):
                result_dict[column_name] = value
            result_list.append(result_dict)

        conn.close()
        return result_list
    except mysql.connector.Error as e:
        return {'error': str(e)}, 400  # Handle database errors
    except Exception as e:
        return {'error': str(e)}, 500  # Handle other exceptions

def call_post_api(url,data,refno):
    try:
        print(url)
        result = {
        "gm_transaction_id": refno,
        "vehicle_numberplate_b64": data['numberPlateImageb64'],
        "vehicle_image_b64": data['vehicleImageb64'],
        "cardId": data['cardId'],
        "dateOfTransaction": data['dateOfTransaction'],
        "plate_path": data['numberPlateImage']
        }
        # Define the file to upload
        files = {
        "vehicle_numberplate": open(data['numberPlateImage'], "rb"),
        "vehicle_image": open(data['vehicleImage'], "rb")
        }

        # Send the POST request with form data and the file
        response = requests.post(url, data=result, files=files)

        # Check the response
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Read the image binary data
            image_binary = image_file.read()
            # Encode the binary data as base64
            base64_encoded = base64.b64encode(image_binary).decode('utf-8')

            return base64_encoded
    except Exception as e:
        print(f"Error converting image to base64: {str(e)}")
        return None


sql_quary_get_vehcle_details = """SELECT vt.id id,vt.machineId machineId, vt.DeviceId deviceId,vt.CardId cardId,vt.dateOfTransaction dateOfTransaction,
vti.VehicleImage vehicleImage, vti.VehicleImage numberPlateImage,'' numberPlateImageb64,'' vehicleImageb64
FROM VehicleTransaction vt
INNER JOIN VehicleTransactionImage vti ON vt.id = vti.VehicleTransactionId
WHERE dateOfTransaction BETWEEN  DATE_ADD('{0}', INTERVAL -180 SECOND)  AND  '{0}'

order by DateOfTransaction desc limit 1"""

def check_active_requests(url):
    RequestVehicle = dbgetlasttransactions("select * from RequestVehicle where isActive = 1")

    if RequestVehicle != []:
        for i in RequestVehicle:
            refno = i['RefNo']
            data = dbgetlasttransactions(sql_quary_get_vehcle_details.format(i['RefNoDatetime']))
            if data != []:
                for veh_details in data:
                    veh_details['dateOfTransaction'] = veh_details['dateOfTransaction'].strftime("%Y-%m-%dT%H:%M:%S")
                    veh_details['numberPlateImageb64'] = convert_image_to_base64(veh_details['numberPlateImage'])
                    veh_details['vehicleImageb64'] = convert_image_to_base64(veh_details['vehicleImage'])



                    api_Responce = call_post_api(url, veh_details, refno)

                    if api_Responce == True:

                        db_update_record(f"update RequestVehicle set isActive = 0 where id = {i['Id']}")

    return 'suss'
