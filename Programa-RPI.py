import base64
import serial
import time
import pigpio

#Programa: Codigo para envio de datos a la RPI (Instrucciones).
#Autor: Carlo Sanchinelli

#Funcion para Enviar Datos con softserial
def softsend(softserial, data):

    softserial.wave_clear()
    softserial.wave_add_serial(27,9600,data)
    mensaje=softserial.wave_create()
    softserial.wave_send_once(mensaje)
    while softserial.wave_tx_busy():
        pass
    softserial.wave_delete(mensaje)

# Inicializacion de la Comunicacion Serial
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0.1
)

#Crear Software Serial
softserial = pigpio.pi()
softserial.set_mode(17,pigpio.INPUT)
softserial.set_mode(27,pigpio.OUTPUT)

pigpio.exceptions = False
softserial.bb_serial_read_close(17)
pigpio.exceptions = True

softserial.bb_serial_read_open(17,9600,8)

n = 0
indata1 = b'a'
ser.flushInput()
# Obtener Datos del Cliente
while True:
    (count,indata) = softserial.bb_serial_read(17) 
    if count:
        if count > 1:
            datos = [indata[i:i+1] for i in range(0, len(indata),1)]
            i = 0
            while i< len(datos):
                print datos[i]
                softsend(softserial,indata)
                i = i + 1
        else:
            if indata != indata1:
                print(indata)
                softsend(softserial,indata)
                indata1 = indata

    if n == 60000:
        data = ser.read(32)
        if data:
            print data
            ser.write(data)
        n = 0
    n = n + 1
