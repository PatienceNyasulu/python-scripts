from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import obd
import time

# OBD Globals
obdRunning = True
obdAvailable = False
engine_power = 0
coolant_temperature = 0
fuel_level = 0
engine_load = 0
ambient_air_temperature = 0
rpm = 0
intake_manifold_pressure = 0
maf = 0
long_term_fuel_trim = 0
short_term_fuel_trim = 0
fuel_pressure = 0
speed = 0
dtc_number = 0
throttle_position = 0
timing_advance = 0
vehicle_identification_number = ""

# Initialize MQTT client
iot_client = AWSIoTMQTTClient("raspberry")
iot_client.configureEndpoint("a3s1cqgu0ggloe-ats.iot.eu-central-1.amazonaws.com", 8883)
iot_client.configureCredentials("AmazonRootCA1.pem", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-private.pem.key", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-certificate.pem")

# Configure MQTT connection
iot_client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
iot_client.configureDrainingFrequency(2)  # Draining: 2 Hz
iot_client.configureConnectDisconnectTimeout(10)  # 10 sec
iot_client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT Core
iot_client.connect()

# OBD Thread
def obd_thread():
    global obdRunning, obdAvailable, engine_power, coolant_temperature, fuel_level, engine_load, ambient_air_temperature, rpm, intake_manifold_pressure, maf, long_term_fuel_trim, short_term_fuel_trim, fuel_pressure, speed, dtc_number, throttle_position, timing_advance, vehicle_identification_number
    obdConnection = obd.OBD()
    print("OBD connected")
    while obdRunning:
        try:
            engine_power = obdConnection.query(obd.commands.ENGINE_POWER).value.magnitude
            coolant_temperature = obdConnection.query(obd.commands.COOLANT_TEMP).value.magnitude
            fuel_level = obdConnection.query(obd.commands.FUEL_LEVEL).value.magnitude
            engine_load = obdConnection.query(obd.commands.ENGINE_LOAD).value.magnitude
            ambient_air_temperature = obdConnection.query(obd.commands.AMBIANT_AIR_TEMP).value.magnitude
            rpm = obdConnection.query(obd.commands.RPM).value.magnitude
            intake_manifold_pressure = obdConnection.query(obd.commands.INTAKE_PRESSURE).value.magnitude
            maf = obdConnection.query(obd.commands.MAF).value.magnitude
            long_term_fuel_trim = obdConnection.query(obd.commands.LONG_FUEL_TRIM).value.magnitude
            short_term_fuel_trim = obdConnection.query(obd.commands.SHORT_FUEL_TRIM).value.magnitude
            fuel_pressure = obdConnection.query(obd.commands.FUEL_PRESSURE).value.magnitude
            speed = obdConnection.query(obd.commands.SPEED).value.magnitude
            dtc_number = obdConnection.query(obd.commands.DTC_NUMBER).value.magnitude
            throttle_position = obdConnection.query(obd.commands.THROTTLE_POS).value.magnitude
            timing_advance = obdConnection.query(obd.commands.TIMING_ADVANCE).value.magnitude
            vehicle_identification_number = obdConnection.query(obd.commands.VIN).value
            obdAvailable = True
        except Exception as e:
            print("An error occurred:", e)
            obdAvailable = False
        time.sleep(0.5)

# Execute the OBD thread
obd_thread()
