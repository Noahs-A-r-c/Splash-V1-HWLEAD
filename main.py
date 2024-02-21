# main.py

import time
from http_functions import *
from ble_functions import *
from csv_to_json import *

# Define global variables to store data received from BLE device, updated in ReadDelegate
received_data = None


def main():
    # MAC address of the BLE device to connect to
    device_mac_address = "60:B6:E1:E1:C2:94"

    # URL to send the HTTP request to
    url = "http://example.com/api"

    # Establish connection with the BLE device
    ble_module = ble_connection_init(device_mac_address)

    # Setup notification handling using ReadDelegate from ble_functions module
    ble_module.withDelegate(ble_functions.ReadDelegate())

    try:
        while True:
            # Send a request for information
            characteristics = ble_module.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb").getCharacteristics()[0]
            characteristics.write(bytes("r", "utf-8"))
            time.sleep(1)  # Wait for a response

            # Check if data has been received from the BLE device
            if received_data:
                # Convert received data to json
                json_data = csv_to_json(received_data)

                # Send HTTP request with the received data
                send_http_request(url, json_data)
                received_data = None  # Reset received_data after sending the HTTP request
    except KeyboardInterrupt:
        # Disconnect from the BLE device on keyboard interrupt
        ble_module.disconnect()

if __name__ == "__main__":
    main()

