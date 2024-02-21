# http_functions.py


# Function to send HTTP request with the received data
def send_http_request(url, data):
    # Construct the request payload
    payload = {"data": data}

    # Send the HTTP request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("HTTP request sent successfully")
    else:
        print("Failed to send HTTP request")
