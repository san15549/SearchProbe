//Librerias 
#include <Servo2.h>
#include <AX12A.h>
#include <SoftwareSerial.h>
#include <MQ135.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <TinyGPS.h>

#define DirectionPin  (6u)
#define BaudRate    (9600ul)
#define ID    (1u)
#define ID2   (2u)

//Actuadores
Servo Servo1;
Servo Servo2;
bool estado=false;
char command = '0';
int mov = 0;
float ang1 = (90-55)/30;
float ang2 = (150-110)/30;
float ang1_nuevo, ang2_nuevo;

//Sensores
SoftwareSerial mySerial(8, 7); // RX,TX
SoftwareSerial mySerial2(11,12); // RX,TX
char sensores[33] = "################################"; //gas(5),imu(8),temp(4),gps(15)
MQ135 GasSensor(A0);
MPU6050 IMU;
OneWire oneWire(4);
DallasTemperature temperatura(&oneWire);
TinyGPS gps;
int n = 0;
float CO2ppm = 0.0;
float temp = 0.0;
float lat, lon;
char Buffer[20];

//Valores Raw - IMU
int ax, ay, az;
int gx, gy, gz;
int i=0;
long tiempo_prev;
float dt;
float ang_x, ang_y;
float ang_x_prev, ang_y_prev;

void setup() {
  //Inicializar Conexiones Seriales
  Serial.begin(9600);
  mySerial.begin(9600);
  mySerial2.begin(9600);
  temperatura.begin();

  //Inicializar I2C
  Wire.begin();
  IMU.initialize();
  
  //Inicializar Motores
  ax12a.begin(BaudRate, DirectionPin, &Serial1);
  ax12a.setEndless(ID, ON);
  ax12a.setEndless(ID2, ON);
  //Inicializar Servos
  Servo1.attach(9);
  Servo2.attach(10);
  Servo1.write(90);
  Servo2.write(110);

  delay(10000);
}

void loop() {
  //Busca si hay instrucciones enviadas
  if (mySerial2.available() > 0) {
    // Leer el comando del usuario
    command = mySerial2.read();
    //Comandos
    //Detenerse
    if (command == '0'){
      ax12a.turn(ID, RIGHT, 0);
      ax12a.turn(ID2, LEFT, 0);
    }
    //Adelante
    if (command == '1'){
      ax12a.turn(ID, RIGHT, 1000);
      ax12a.turn(ID2, LEFT, 1000);
    }
    //Atras
    if (command == '2'){
      ax12a.turn(ID, LEFT, 1000);
      ax12a.turn(ID2, RIGHT, 1000);
    }
    //Izquierda
    if (command == '3'){
      ax12a.turn(ID, RIGHT, 1000);
      ax12a.turn(ID2, LEFT, 0);
    }
    //Derecha
    if (command == '4'){
      ax12a.turn(ID, RIGHT, 0);
      ax12a.turn(ID2, LEFT, 1000);
    }
    //Modo de Operación
    if (command == '5'){
      estado=!estado;
      if (estado==true){
        mov = 0;
        ang1_nuevo = 90;
        ang2_nuevo = 110;
        while (mov < 31){
          ang1_nuevo = ang1_nuevo - ang1;
          ang2_nuevo = ang2_nuevo + ang2; 
          Servo1.write(ang1_nuevo);
          Servo2.write(ang2_nuevo);
          mov=mov+1;
          delay(25);
        }
        mov = 0;
      }
      if (estado==false){
        mov = 0;
        ang1_nuevo = 55;
        ang2_nuevo = 150;
        while (mov < 31){
          ang1_nuevo = ang1_nuevo + ang1;
          ang2_nuevo = ang2_nuevo - ang2;
          Servo1.write(ang1_nuevo);
          Servo2.write(ang2_nuevo);
          mov=mov+1;
          delay(25);
        }
        mov = 0;
      }
      command = '0';
    }
    //Adelante-Derecha
    if (command == '6'){
      ax12a.turn(ID, RIGHT, 500);
      ax12a.turn(ID2, LEFT, 1000);
    }
    //Adelante-Izquierda
    if (command == '7'){
      ax12a.turn(ID, RIGHT, 1000);
      ax12a.turn(ID2, LEFT, 500);
    }   
  }
  if (n==1000){
    lectura_gas();
  }
  if (n==2000){
    lectura_IMU();
  }
  if (n==3000){
    lectura_temp();
  }
  if (n==4000){
    lectura_gps();
    mySerial2.write(sensores);
    n = 0;
  }
  n = n + 1;
  delay(1);
}

void lectura_gas() {
  //GAS (5)
  CO2ppm = 116.6020682 * pow((GasSensor.getResistance()/205.0), -2.769034857);
  dtostrf(CO2ppm, 0, 2, Buffer);
  if (Buffer[4] == '\0'){
    sensores[0] = 'G';
    sensores[1] = 'G';
    sensores[2] = 'G';
    sensores[3] = 'G';
    sensores[4] = 'G';
  }
  else{
    sensores[0] = Buffer[0];
    sensores[1] = Buffer[1];
    sensores[2] = Buffer[2];
    sensores[3] = Buffer[3];
    sensores[4] = Buffer[4];
  }
}

void lectura_IMU() {
  //IMU (8)
  IMU.getAcceleration(&ax, &ay, &az);
  IMU.getRotation(&gx, &gy, &gz);
  dt = (millis()-tiempo_prev)/1000.0;
  tiempo_prev=millis();
  float accel_ang_x=atan(ay/sqrt(pow(ax,2) + pow(az,2)))*(180.0/3.14);
  float accel_ang_y=atan(-ax/sqrt(pow(ay,2) + pow(az,2)))*(180.0/3.14);
  ang_x = 0.98*(ang_x_prev+(gx/131)*dt) + 0.02*accel_ang_x;
  ang_y = 0.98*(ang_y_prev+(gy/131)*dt) + 0.02*accel_ang_y;
  ang_x_prev=ang_x;
  ang_y_prev=ang_y;
  dtostrf(ang_x, 0, 2, Buffer);
  if (Buffer[3] == '\0'){
    sensores[5] = 'X';
    sensores[6] = 'X';
    sensores[7] = 'X';
    sensores[8] = 'X';
  }
  else{
    sensores[5] = Buffer[0];
    sensores[6] = Buffer[1];
    sensores[7] = Buffer[2];
    sensores[8] = Buffer[3];
  }
  dtostrf(ang_y, 0, 2, Buffer);
  if (Buffer[3] == '\0'){
    sensores[9] = 'Y';
    sensores[10] = 'Y';
    sensores[11] = 'Y';
    sensores[12] = 'Y';
  }
  else{
    sensores[9] = Buffer[0];
    sensores[10] = Buffer[1];
    sensores[11] = Buffer[2];
    sensores[12] = Buffer[3];
  }
}

void lectura_temp() {
  //TEMPERATURA (4)
  temperatura.requestTemperatures();
  temp = temperatura.getTempCByIndex(0);
  dtostrf(temp, 0, 2, Buffer);
  if (Buffer[3] == '\0'){
    sensores[13] = 'T';
    sensores[14] = 'T';
    sensores[15] = 'T';
    sensores[16] = 'T';
  }
  else{
    sensores[13] = Buffer[0];
    sensores[14] = Buffer[1];
    sensores[15] = Buffer[2];
    sensores[16] = Buffer[3];
  }
}

void lectura_gps() {
  //GPS (15)
  bool gps_ready = false;
  if (mySerial.available()){
    char c = mySerial.read();
    if (gps.encode(c)) {
      gps_ready = true;
    }
  }
  if (gps_ready){
    gps.f_get_position(&lat,&lon);
    dtostrf(lat, 0, 5, Buffer);
    sensores[17] = Buffer[0];
    sensores[18] = Buffer[1];
    sensores[19] = Buffer[2];
    sensores[20] = Buffer[3];
    sensores[21] = Buffer[4];
    sensores[22] = Buffer[5];
    sensores[23] = Buffer[6];
    dtostrf(lon, 0, 5, Buffer);
    sensores[24] = Buffer[0];
    sensores[25] = Buffer[1];
    sensores[26] = Buffer[2];
    sensores[27] = Buffer[3];
    sensores[28] = Buffer[4];
    sensores[29] = Buffer[5];
    sensores[30] = Buffer[6];
    sensores[31] = Buffer[7];
  }
  else{
    sensores[17] = 'L';
    sensores[18] = 'L';
    sensores[19] = 'L';
    sensores[20] = 'L';
    sensores[21] = 'L';
    sensores[22] = 'L';
    sensores[23] = 'L';
    sensores[24] = 'L';
    sensores[25] = 'L';
    sensores[26] = 'L';
    sensores[27] = 'L';
    sensores[28] = 'L';
    sensores[29] = 'L';
    sensores[30] = 'L';
    sensores[31] = 'L';
  }
}
