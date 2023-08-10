import board
import busio
import adafruit_gps
import serial
import sys
import datetime
import pandas as pd
import time
import csv
import threading
uart = None
gps  = None
data = None
def gps_read():
    global data, gps
    data = gps.read(185)

#Función que escribe la última linea en el csv  ruta_archivo
def escribir(ruta_archivo, nueva_fila):
    # Leer el archivo CSV existente)
    df = pd.DataFrame(nueva_fila)
    df = df.T
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(ruta_archivo,mode="a",header =False, index=False)

#Procesa la data de gps para tener los datos importantes en una lista
def data_processing(data_string):
    list_data = data_string.split()
    GNGGA = list_data[3].split(',')
    GNRMC = list_data[4].split(',')
    data2 = GNGGA[9:11]
    data1 = GNRMC[1:8]
    for i in data2:
      data1.append(i)
    return data1

#Función que extrae la última linea de un csv
def line_csv(file_csv):
    with open(file_csv,'r') as archivo:
      read_csv = csv.reader(archivo)
      for line in read_csv:
           last_line =  line
      return last_line
# hora, estado, lat, ns, long, we, vel, alt, met
def main():
    global gps, data, uart
    now = datetime.datetime.now()
    name = now.strftime("%m-%d-%H-%M-%S")
    logfile = f"/home/pi/log/log{name}.txt"

    uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=10)
    gps = adafruit_gps.GPS(uart)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    reader = threading.Thread(target=gps_read)
    reader.start()
    reader.join(10)
    data = gps.read(185)
    
    if data is not None:
        #Escritura mensaje principal
        data_string = "".join([chr(b) for b in data])
        if data_string == "" or data_string == None:
            return [0.0, "v", 0.0, "s", 0.0, "w", 0.0, 0.0, "m"] 

        print(f"Este es el data string! :{data_string}")
        procesado = [0.0, "v", 0.0, "s", 0.0, "w", 0.0, 0.0, "m"] 
        try:
            procesado = data_processing(data_string)
            return procesado
        except Exception:
            print("valor default!")
        return procesado
    return [0.0, "v", 0.0, "s", 0.0, "w", 0.0, 0.0, "m"] 


if __name__ == "__main__":
    main()
