import sys, os
import mpu6050
import bmp180
import aht10
import gps_bueno
import time

if __name__ == "__main__":
	DT=30
	_, x, y = sys.argv
	while True:
		mpu6050.main()
		bmp180.main()
		aht10.main()
		gps_bueno.main(x, y)
		time.sleep(DT)


