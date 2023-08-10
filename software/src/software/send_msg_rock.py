# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import serial
import time
import csv
from adafruit_rockblock import RockBlock
import csv
uart = serial.Serial("/dev/serial0",19200)

def line_csv(file_csv):
    with open(file_csv, 'r') as archivo:
        # Lee el archivo CSV utilizando el lector de CSV de Python
        read_csv = csv.reader(archivo)
        # Itera sobre las líneas del archivo CSV
        for line in read_csv:
            last_line = line
        return last_line

def main(pack_msg):
    rb = RockBlock(uart)
    #last_line = line_csv(file_csv)
    rb.data_out = pack_msg
    retry = 0
    print("Hablando con le moooooon")
    status = rb.satellite_transfer()
    while status[0] > 8 and retry < 10:
        time.sleep(1)
        status = rb.satellite_transfer()
        print(f"retrying! {retry}")
        retry+=1
    print("Done!")

