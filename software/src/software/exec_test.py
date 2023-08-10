import sys, os
import mpu6050
import bmp180
import aht10
import gps_final
import send_msg_rock
from struct import pack, unpack
#import send_message_prin
#import secd_message_sec
import time
FILE_CSV = "./logfile.csv"
FORMAT_PRIN = "fcfcfcffcfff"
FORMAT_SEC = "fffffff"
if __name__ == "__main__":
    DT=2
    msg = None
    while True:
        for _ in range(DT):
            t0 = time.time()
            #Gx, Gy, Gz, Ax, Ay, Az = mpu6050.main()
            Gx, Gy, Gz, Ax, Ay, Az = 0,0,0,0,0,0 #Datos de placeholder
            print("sacando la temperataura")
            temp, pres, _ = bmp180.main()
            print("listo la temp")
            _, hum = aht10.main()
            #_, hum= 0,0.0 #Datos de placeholder
            print("sacando el gps")
            hora, estado, lat, ns, lng, we, vel, alt, m = gps_final.main()
            print("gps obtenido!")
            #Definimos los mensajes:
            msg2log_prin = f"{hora},{estado},{lat},{ns},{lng},{we},{vel},{alt},{m},{temp},{hum},{pres}"
            msg2log_sec =f"{Gx},{Gy},{Gz},{Ax},{Ay},{Az}"
            with open(FILE_CSV, "a") as f:
                f.write(f"{msg2log_prin},{msg2log_sec}\n")
            msg = msg2log_prin
            print(msg)
            tf = time.time()
            print(tf - t0)
            time.sleep(min(21 - (tf - t0), 21))
        packed_msg_prin = pack(FORMAT_PRIN, hora, estado[0].encode(), lat, ns[0].encode(), lng, we[0].encode(), vel, alt, m[0].encode(), temp, pres, hum)
        packed_msg_sec = pack(FORMAT_SEC, hora, Gx, Gy, Gz, Ax, Ay, Az)
        #send_msg_rock.main(packed_msg_prin)
        #send_msg_rock.main(packed_msg_sec)
        #send_message_prin.main() #<- se manda ultima linea de mensaje_principal.csv
        #send_message_sec.main()  #<- se manda ultima linea de mensaje_secundario.csv
