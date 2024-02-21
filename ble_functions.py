# ble_funct.py

import bluepy.btle as btle
import time

def ble_connection_init(mac_address):
    """
    Establishes a connection with a BLE device.

    Args:
    - mac_address: The MAC address of the BLE device to connect to.

    Returns:
    - ble_module: The Peripheral object representing the BLE connection.
    """
    connected = False
    fail_count = 0

    while not connected:
        try:
            ble_module = btle.Peripheral(mac_address)
            connected = True
            print("Connected to (",mac_address,")")

        except:
            fail_count += 1
            print(f"Connection failed, retrying ({fail_count})")
            time.sleep(0.5)

    return ble_module

class ReadDelegate(btle.DefaultDelegate):
    """
    Class to handle notifications received from the BLE device.
    """
    def handleNotification(self, cHandle, data):
        global received_data # access the global variable
        """
        Process the received notification data.

        Args:
        - cHandle: The handle of the characteristic sending the notification.
        - data: The notification data received.
        """
        data_string = data.decode("utf-8")
        print("Received notification:", data_string)

        received_data = data_string

def ble_notification_handler_init(ble_module):
    """
    Configures the ReadDelegate instance to handle notifications asynchronously.

    Args:
    - ble_module: The Peripheral object representing the BLE connection.
    """
    ble_module.withDelegate(ReadDelegate())

def ble_request_info(characteristics):
    """
    Sends a request for information to the BLE device.

    Args:
    - characteristics: The characteristics associated with the BLE service.
    """
    characteristics.write(bytes("r", "utf-8"))


# main code for testing:

def main():
    # MAC address of the BLE device to connect to
    device_mac_address = "60:B6:E1:E1:C2:94"

    # Establish connection with the BLE device
    ble_module = ble_connection_init(device_mac_address)

    # Retrieve necessary information for communication
    service_uuid = ble_module.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
    characteristics = service_uuid.getCharacteristics()[0]

    # Setup notification handling
    ble_notification_handler_init(ble_module)

    try:
        while True:
            # Send a request for information
            ble_request_info(characteristics)
            time.sleep(1)  # Wait for a response
    except KeyboardInterrupt:
        # Disconnect from the BLE device on keyboard interrupt
        ble_module.disconnect()

if __name__ == "__main__":
    main()
