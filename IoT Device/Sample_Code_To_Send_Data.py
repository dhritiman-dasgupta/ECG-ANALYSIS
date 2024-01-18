from azure.iot.device import IoTHubDeviceClient, Message
import json
# Define the connection string
connection_string = "HostName=EcgAcqusitioDev.azure-devices.net;DeviceId=mc01;SharedAccessKey=3srREAOyBBE/7N1DsKWIpwIBoM8deiKO4AIoTBiG8aU="

# Create an IoT Hub client
client = IoTHubDeviceClient.create_from_connection_string(connection_string)

# Define the data payload
device_id = "MC02"
data = [(0, 1.23), (1, 1.233), (2, 1.243), (3, 1.223), (4, 1.243), (5, 1.233), (6, 1.23098), (7, 1.223), (8, 1.23), (9, 1.213), (10, 1.734)]
payload = {"device_id": device_id, "data": data}

# Convert the payload to a JSON string
message = Message(json.dumps(payload))

# Send the message to IoT Hub
client.send_message(message)
print("Message sent to IoT Hub")

# Optionally, listen for messages from IoT Hub
def message_listener(message):
    print("Received message from IoT Hub:", message.data)

client.on_message_received = message_listener

# Start the client
client.connect()
input("Press Enter to exit...\n")
client.disconnect()
