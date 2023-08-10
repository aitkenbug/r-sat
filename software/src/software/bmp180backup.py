# ------ PINS ------
# VCC/VIN -> 3.3V (PIN 1)
# GND -> GND (PIN 6)
# SCL -> SCL (PIN 5)
# SDA -> SDA (PIN 3)
import csv
import bmpsensor
import time
import datetime
import pytz

# Nombre del archivo CSV
nombre_archivo = 'data_bmp180.csv'
zona_horaria_utc = pytz.utc
def main():
    # Ciclo de captura y escritura de datos
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
	    escritor_csv = csv.writer(archivo_csv)
	    escritor_csv.writerow(['Temp', 'Pressure', 'Altitud'])  # Escribir encabezados de columna

	    temp, pressure, altitude = bmpsensor.readBmp180()
	    hora_utc = datetime.datetime.now(tz=zona_horaria_utc).strftime('%H%M%S')

	    escritor_csv.writerow([hora_utc,temp, pressure, altitude])
	    archivo_csv.flush()  # Vaciar el búfer y asegurarse de que se escriban los datos en el archivo
    return temp, pressure, altitude

