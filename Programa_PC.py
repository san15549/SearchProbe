from PyQt5 import QtGui, QtTest, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame
from PyQt5.QtGui import QPixmap
import sys
import keyboard
import base64
import serial
import time

#Programa: Código para envio y recibo de datos con la RPI.
#Autor: Carlo Sanchinelli

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "GUI - Robot de Rescate"
        self.top = 100
        self.left = 100
        self.width = 1200
        self.height = 600

    def InitWindow(self):
        #Label - Titulo Principal
        self.titulo = QLabel(self)
        self.titulo.setGeometry(100,10,581,51)
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.titulo.setFont(font)
        self.titulo.setText("ROBOT DE OPERACIONES DE BÚSQUEDA Y RESCATE")
        #Label - Titulo Camara
        self.titulo_camara = QLabel(self)
        self.titulo_camara.setGeometry(40,70,71,21)
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        self.titulo_camara.setFont(font)
        self.titulo_camara.setText("Cámara:")
        #Label - Titulo Comandos
        self.titulo_comandos = QLabel(self)
        self.titulo_comandos.setGeometry(380,70,91,21)
        self.titulo_comandos.setFont(font)
        self.titulo_comandos.setText("Comandos:")
        #Label - Titulo Operacion
        self.titulo_operacion = QLabel(self)
        self.titulo_operacion.setGeometry(380,310,171,21)
        self.titulo_operacion.setFont(font)
        self.titulo_operacion.setText("Modo de Operación:")
        #Label - Titulo Sensores
        self.titulo_sensores = QLabel(self)
        self.titulo_sensores.setGeometry(700,70,71,21)
        self.titulo_sensores.setFont(font)
        self.titulo_sensores.setText("Sensores:")
        #Label - Titulo Temperatura
        self.titulo_temperatura = QLabel(self)
        self.titulo_temperatura.setGeometry(700,110,131,21)
        self.titulo_temperatura.setFont(font)
        self.titulo_temperatura.setText("TEMPERATURA:")
        #Label - Titulo Angulo2
        self.titulo_angulo2 = QLabel(self)
        self.titulo_angulo2.setGeometry(900,300,101,21)
        self.titulo_angulo2.setFont(font)
        self.titulo_angulo2.setText("ÁNGULO θ:")
        #Label - Titulo Angulo1
        self.titulo_angulo1 = QLabel(self)
        self.titulo_angulo1.setGeometry(900,230,101,21)
        self.titulo_angulo1.setFont(font)
        self.titulo_angulo1.setText("ÁNGULO ϕ:")
        #Label - Titulo Latitud
        self.titulo_latitud = QLabel(self)
        self.titulo_latitud.setGeometry(700,410,81,21)
        self.titulo_latitud.setFont(font)
        self.titulo_latitud.setText("LATITUD:")
        #Label - Titulo Longitud
        self.titulo_longitud = QLabel(self)
        self.titulo_longitud.setGeometry(880,410,101,21)
        self.titulo_longitud.setFont(font)
        self.titulo_longitud.setText("LONGITUD:")
        #Label - Titulo CO2
        self.titulo_co2 = QLabel(self)
        self.titulo_co2.setGeometry(690,160,141,21)
        self.titulo_co2.setFont(font)
        self.titulo_co2.setText("NIVEL DE CO2:")



        #Label - Imagen Comandos
        self.comandos = QLabel(self)
        #self.comandos.setFrameShape(QFrame.Panel)
        #self.comandos.setLineWidth(1)
        self.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsOff.jpg"))
        self.comandos.setGeometry(380,100,240,200)
        #Label - Imagen Camara
        self.camara = QLabel(self)
        self.camara.setFrameShape(QFrame.Panel)
        self.camara.setLineWidth(1)
        self.camara.setPixmap(QPixmap("ImagenesGUI\CameraOff.jpg"))
        self.camara.setGeometry(40,100,281,281)
        #Label - Imagen Operacion
        self.operacion = QLabel(self)
        #self.operacion.setFrameShape(QFrame.Panel)
        #self.operacion.setLineWidth(1)
        self.operacion.setPixmap(QPixmap("ImagenesGUI\OperationOff.jpg"))
        self.operacion.setGeometry(380,340,141,121)
        #Label - Imagen Angulos
        self.angulos = QLabel(self)
        #self.angulos.setFrameShape(QFrame.Panel)
        #self.angulos.setLineWidth(1)
        self.angulos.setPixmap(QPixmap("ImagenesGUI\Inclination.jpg"))
        self.angulos.setGeometry(690,210,193,174)


        #Label - Latitud
        self.latitud = QLabel(self)
        self.latitud.setGeometry(700,430,131,31)
        self.latitud.setFont(font)
        self.latitud.setText("")
        #Label - Longitud
        self.longitud = QLabel(self)
        self.longitud.setGeometry(880,430,131,31)
        self.longitud.setFont(font)
        self.longitud.setText("")
        #Label - Angulo1
        self.angulo1 = QLabel(self)
        self.angulo1.setGeometry(900,260,131,31)
        self.angulo1.setFont(font)
        self.angulo1.setText("")
        #Label - Angulo2
        self.angulo2 = QLabel(self)
        self.angulo2.setGeometry(900,330,131,31)
        self.angulo2.setFont(font)
        self.angulo2.setText("")
        #Label - Temperatura
        self.temperatura = QLabel(self)
        self.temperatura.setGeometry(840,105,131,31)
        self.temperatura.setFont(font)
        self.temperatura.setText("")
        #Label - co2
        self.co2 = QLabel(self)
        self.co2.setGeometry(840,155,131,31)
        self.co2.setFont(font)
        self.co2.setText("")
        
        

        #Window - Main Window
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top,self.left,self.width,self.height)

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        
        self.setPalette(palette)
        self.show()

# Inicializacion de la Interfaz
App = QApplication([])
window = Window()
window.InitWindow()
QtTest.QTest.qWait(1000)
window.operacion.setPixmap(QPixmap("ImagenesGUI\OperationNormal"))

# Inicializacion de la Comunicacion Serial
ser = serial.Serial(
    port='COM16',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0.1
)

# Programa Principal
estado = True
estado2 = 1
command = b'0'
command1 = b'a'
estadotemp = True
n = 0
ser.reset_input_buffer()
while True:
    QtTest.QTest.qWait(1)

    if keyboard.is_pressed('up'):
        if keyboard.is_pressed('right'):
            command = b'6'
            window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsUpRight.jpg"))
        elif keyboard.is_pressed('left'):
            command = b'7'
            window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsUpLeft.jpg"))
        else:
            command = b'1'
            window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsUp.jpg"))
    elif keyboard.is_pressed('down'):
        command = b'2'
        window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsDown.jpg"))
    elif keyboard.is_pressed('left'):
        command = b'3'
        window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsLeft.jpg"))
    elif keyboard.is_pressed('right'):
        command = b'4'
        window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsRight.jpg"))
    elif keyboard.is_pressed('spacebar'):
        command = b'5'
        if estado == False:
            if estado2 == 1:
                window.operacion.setPixmap(QPixmap("ImagenesGUI\OperationNormal.jpg"))
                estado = True
                estado2 = 0
        else:
            if estado2 == 1:
                window.operacion.setPixmap(QPixmap("ImagenesGUI\OperationInclinado.jpg"))
                estado = False
                estado2 = 0
    else:
        command = b'0'
        estado2 = 1
        window.comandos.setPixmap(QPixmap("ImagenesGUI\CommandsOff.jpg"))

    if command !=command1:
        ser.write(command)
        command1 = command

    if n == 2000:
        print('Leyendo')
        sensores = ser.read(32)
        sensores = sensores.decode("utf-8")
        if sensores:
            co2 = (sensores)[0:5]
            window.co2.setText(co2)
            roll = (sensores)[5:9]
            window.angulo1.setText(roll)
            pitch = (sensores)[9:13]
            window.angulo2.setText(pitch)
            temp = (sensores)[13:17]
            window.temperatura.setText(temp)
            lat = (sensores)[17:24]
            window.latitud.setText("14.6054")
            lon = (sensores)[24:]
            window.longitud.setText("-90.4882")
        n = 0

    n = n + 1
    
