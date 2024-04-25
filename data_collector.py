from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import obd
import time

# Configure MQTT client
iot_client = AWSIoTMQTTClient("raspberry")
iot_client.configureEndpoint("a3s1cqgu0ggloe-ats.iot.eu-central-1.amazonaws.com", 8883)
iot_client.configureCredentials("AmazonRootCA1.pem", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-private.pem.key", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-certificate.pem.crt")

# Configure MQTT connection
iot_client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
iot_client.configureDrainingFrequency(2)  # Draining: 2 Hz
iot_client.configureConnectDisconnectTimeout(10)  # 10 sec
iot_client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT Core
iot_client.connect()

# Initialize OBD connection
connection = obd.OBD()

# OBD2 commands for specific parameters
commands = {
    #"engine_power": obd.commands.ENGINE_POWER,
    "coolant_temperature": obd.commands.COOLANT_TEMP,
    "fuel_level": obd.commands.FUEL_LEVEL,
    "engine_load": obd.commands.ENGINE_LOAD,
    "ambient_air_temperature": obd.commands.AMBIANT_AIR_TEMP,
    "rpm": obd.commands.RPM,
    "intake_manifold_pressure": obd.commands.INTAKE_PRESSURE,
    "maf": obd.commands.MAF,
    "long_term_fuel_trim": obd.commands.LONG_FUEL_TRIM_1,
    "short_term_fuel_trim": obd.commands.SHORT_FUEL_TRIM_1,
    "fuel_pressure": obd.commands.FUEL_PRESSURE,
    "speed": obd.commands.SPEED,
    "dtc_number": obd.commands.GET_DTC,
    "throttle_position": obd.commands.THROTTLE_POS,
    "timing_advance": obd.commands.TIMING_ADVANCE,
    "vehicle_identification_number": obd.commands.VIN,
    "equivalent_ratio": obd.commands.EQUIV_RATIO
}

# Main loop to read and publish OBD2 data
while True:
    for param_name, cmd in commands.items():
        try:
            response = connection.query(cmd)
            if response.is_null():
                continue
            data = f"{param_name}: {response.value}"
            print(data)  # Optionally print the data
            iot_client.publish("obd2_data", data, 1)
        except Exception as e:
            print(f"Error reading {param_name}: {e}")
    time.sleep(10)  # Adjust as needed for data frequency
