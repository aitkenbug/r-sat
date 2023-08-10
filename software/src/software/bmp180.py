# ------ PINS ------
# VCC/VIN -> 3.3V (PIN 1)
# GND -> GND (PIN 6)
# SCL -> SCL (PIN 5)
# SDA -> SDA (PIN 3)
import bmpsensor

def main():
    # Ciclo de captura y escritura de datos 
    temp, pressure, altitude = bmpsensor.readBmp180()
    return temp, pressure, altitude

