#Librerias externas:
import Adafruit_PCA9685 as modulo;	"""Información: https://github.com/adafruit/Adafruit_Python_PCA9685"""
import smbus;						"""Información: https://www.engineersgarage.com/articles-raspberry-pi-i2c-bus-pins-smbus-smbus2-python/"""

#Librerias internas:
from time import sleep;        		"""Información: https://docs.python.org/3/library/time.html"""
import math;						"""Información: https://docs.python.org/3/library/math.html"""

add = 0x68   # Address del sensor (usar "sudo i2cdetect -y 1" en la terminar para detectar la dirección de los componentes i2c)

#Iniciar PCA9685 con su default address (0x40)	
pwm = modulo.PCA9685(0x40)

#Configurar los pulsos
puls_0 = 100
puls_180 = 500

#Setear la frecuencia de los servos
pwm.set_pwm_freq(50)

#tiempo entre movimientos (segundos):
t = 1


def girar(angulo):
	return  int(puls_0 + (angulo/180)*(puls_180-puls_0))

	
try:
	while True:	
		print("0")
		pwm.set_pwm(0, 0, girar(0))
		sleep(t)
		print("90")
		pwm.set_pwm(0, 0, girar(90))
		sleep(t)
		print("180")
		pwm.set_pwm(0, 0, girar(180))
		sleep(t)
				
		
		
except KeyboardInterrupt:
	for i in range(15):
		pwm.set_pwm(i, 0, 0)
