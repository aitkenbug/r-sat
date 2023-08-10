import smbus					#import SMBus module of I2C
import time         #import
import csv

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
Device_Address = 0x68   # MPU6050 device address


def MPU_Init(bus):
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr, bus):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def main():
    bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

    MPU_Init(bus)

	# print (" Reading Data of Gyroscope and Accelerometer")

	# while True:

	# #Read Accelerometer raw value
	# acc_x = read_raw_data(ACCEL_XOUT_H)
	# acc_y = read_raw_data(ACCEL_YOUT_H)
	# acc_z = read_raw_data(ACCEL_ZOUT_H)

	# #Read Gyroscope raw value
	# gyro_x = read_raw_data(GYRO_XOUT_H)
	# gyro_y = read_raw_data(GYRO_YOUT_H)
	# gyro_z = read_raw_data(GYRO_ZOUT_H)

	# #Full scale range +/- 250 degree/C as per sensitivity scale factor
	# Ax = acc_x/16384.0
	# Ay = acc_y/16384.0
	# Az = acc_z/16384.0

	# Gx = gyro_x/131.0
	# Gy = gyro_y/131.0
	# Gz = gyro_z/131.0


	# print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
	# sleep(1)
    nombre_archivo = 'data_mpu6050.csv'

	# Ciclo de captura y escritura de datos
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
	    escritor_csv = csv.writer(archivo_csv)
	    escritor_csv.writerow(['Gx[°/s]', 'Gy[°/s]', 'Gz[°/s]','Ax[g]', 'Ay[g]', 'Az[g]' ])  # Escribir encabezados de columna
	    #Read Accelerometer raw value
	    acc_x = read_raw_data(ACCEL_XOUT_H, bus)
	    acc_y = read_raw_data(ACCEL_YOUT_H, bus)
	    acc_z = read_raw_data(ACCEL_ZOUT_H, bus)

	    #Read Gyroscope raw value
	    gyro_x = read_raw_data(GYRO_XOUT_H, bus)
	    gyro_y = read_raw_data(GYRO_YOUT_H, bus)
	    gyro_z = read_raw_data(GYRO_ZOUT_H, bus)

	    #Full scale range +/- 250 degree/C as per sensitivity scale factor
	    Ax = acc_x/16384.0
	    Ay = acc_y/16384.0
	    Az = acc_z/16384.0
	    Gx = gyro_x/131.0
	    Gy = gyro_y/131.0
	    Gz = gyro_z/131.0
	    escritor_csv.writerow([Gx, Gy, Gz, Ax, Ay, Az ])
	    archivo_csv.flush()  # Vaciar el búfer y asegurarse de que se escriban los datos en el archivo

    return Gx, Gy, Gz, Ax, Ay, Az
