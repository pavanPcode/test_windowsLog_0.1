def read_data_from_file():
    data = {}

    # Open the file for reading
    with open('Config.txt', 'r') as file:
        for line in file:
            # Split each line into key and value pairs
            key, value = line.strip().split('=')
            # Remove leading and trailing spaces from key and value
            key = key.strip()
            value = value.strip()
            # Store the data in a dictionary
            data[key] = value

    return data