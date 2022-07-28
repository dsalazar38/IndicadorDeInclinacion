import network, time, urequests
import json
from machine import Pin, SoftI2C
from time import sleep
from accel import accel


def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
led = Pin(15, Pin.OUT)
Zum = Pin(18, Pin.OUT)

capture = accel(i2c,0x68)

print("I2C "+ hex(i2c.scan()[0]) )
print("I2C "+ str(i2c.scan()[0]) )

if conectaWifi ("Jasalgon", "Nohaywifi04"):
    
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    url = "http://192.168.80.37:8080/api/Incliancion/save"

    while True:
        mesure= capture.get_values()
        ejez = mesure["AcZ"]

        
        if ejez > 2000 or ejez < -7000:
          led.value(1)
          Zum.value(1)
          print (ejez)
          respuesta = urequests.get(url+"&Angulo="+str(ejez)+"&usuario="+"ana")
          print(respuesta.text)
          print(respuesta.status_code)
          respuesta.close ()
          sleep(0.3)

          
        else:
          led.value(0)
          Zum.value(0)
          print(ejez)
          sleep(0.3)
    
  

    
    