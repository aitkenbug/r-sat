import smbus2
import time
import csv

# AHT10 Registers
AHT10_ADDR = 0x38
AHT10_CMD_INIT = 0xE1
AHT10_CMD_MEASURE = 0xAC
AHT10_STATUS_BUSY = 0x80
AHT10_DATA_MSB = 0x00
AHT10_DATA_LSB = 0x01
AHT10_DATA_XLSB = 0x02



# Initialize the AHT10 sensor
def initialize_sensor(bus):
    bus.write_byte(AHT10_ADDR, AHT10_CMD_INIT)
    time.sleep(0.01)

# Read the status of the AHT10 sensor
def read_status(bus):
    status = bus.read_byte(AHT10_ADDR)
    return status

# Read the temperature and humidity from the AHT10 sensor
def read_temperature_humidity(bus):
    bus.write_byte(AHT10_ADDR, AHT10_CMD_MEASURE)
    time.sleep(0.5)
    
    while read_status(bus) & AHT10_STATUS_BUSY:
        time.sleep(0.1)
    
    data = bus.read_i2c_block_data(AHT10_ADDR, AHT10_DATA_MSB, 6)
    
    raw_humidity = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
    humidity = (raw_humidity / 1048576.0) * 100.0
    
    raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    temperature = (raw_temperature / 1048576.0) * 200.0 - 50.0
    
    return temperature, humidity

def main():
    # Create an SMBus object
    bus = smbus2.SMBus(1)


    # Initialize the sensor
    initialize_sensor(bus)

    # Read and display temperature and humidity
    # temperature, humidity = read_temperature_humidity()
    # print("Temperature: {:.2f}°C".format(temperature))
    # print("Humidity: {:.2f}%".format(humidity))

    # Nombre del archivo CSV
    nombre_archivo = 'data_aht10.csv'

    # Ciclo de captura y escritura de datos
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Temperature', 'Humidity'])  # Escribir encabezados de columna

        temperature, humidity = read_temperature_humidity(bus)

        escritor_csv.writerow([temperature, humidity])
        archivo_csv.flush()  # Vaciar el búfer y asegurarse de que se escriban los datos en el archivo
    return temperature, humidity

if __name__ == "__main__":
	main()
