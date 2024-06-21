#Librerias externas:
import Adafruit_PCA9685 as modulo;	"""Información: https://github.com/adafruit/Adafruit_Python_PCA9685"""
from bluedot import BlueDot;		"""Información: https://bluedot.readthedocs.io/en/latest/gettingstarted.html"""
import smbus;						"""Información: https://www.engineersgarage.com/articles-raspberry-pi-i2c-bus-pins-smbus-smbus2-python/"""

#Librerias internas:
from time import sleep;        		"""Información: https://docs.python.org/3/library/time.html"""
import math;						"""Información: https://docs.python.org/3/library/math.html"""
from signal import pause;			"""Información: https://docs.python.org/3/library/signal.html"""

#Registros y direcciones para el sensor MPU (buscar en datasheet en caso de usar otro modelo)
power = 0x6B
sample_rate = 0x19
conf = 0x1A
gyro_conf = 0x1B
interrup = 0x38
x_dir  = 0x3B
y_dir  = 0x3D
z_dir  = 0x3F

add = 0x68   # Address del sensor (usar "sudo i2cdetect -y 1" en la terminar para detectar la dirección de los componentes i2c)

#Iniciar PCA9685 con su default address (0x40)	
pwm = modulo.PCA9685(0x40)

#Configurar los pulsos de los servos para 0 y 180 grados (calibrado usando los pasos del manual Armado e Iniciación, sección "Calibración de servos")
puls_0 = 100
puls_180 = 500

#Setear la frecuencia de los servos (dependen del servo, checar datasheets)
pwm.set_pwm_freq(50)

"""Vectores de combinaciones posibles:"""
TODO = range(0, 12) 					#El rango va dependiendo de las conexiones de los servos en el modulo PCA9685
	
#Separar por lado  						(revisar documento de conexiones para saber cual es cual)
Izquierda = range(0, 6)
Derecha = range(6, 12)

#Separar por partes
femurs = range(10, -1, -2)
tarsos = range(1, 12, 2)

#Separado partes y lado
femur_I = [0, 2, 4]
tarso_I = [1, 3, 5]
femur_D = [6, 8, 10]
tarso_D = [7, 9, 11]

"""Partes independientes: """ 
FIT, TIT, FIM, TIM, FIB, TIB, FDT, TDT, FDM, TDM, FDB, TDB = TODO
	
#Tiempo entre movimientos (Segundos)
t = 0.08

"""Angulos ideales"""
up_d = 124
up_i = 51
down_d = 110
down_i = 70
delante_i = 105
delante_d = 75
detras_i = 75
detras_d = 105

"""------------------------------------------------------------------------------------------------------------------"""
"""Funciones: """
def girar(angulo):		#Mapeo de angulos 
	return  int(puls_0 + (angulo/180)*(puls_180-puls_0))

def avanzar():			#Avanzar levantando 3 a la vez (ideal si spike puede levantar las patas)
	print("Vuelta izquierda: ")
	print("Levantar tarsos derecha, bajar izquierda")
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(down_i))
	sleep(t)
	#Tarsos derecha
	pwm.set_pwm(TDT, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(up_d))
	sleep(t)
	
	print("Delante femurs derecha, atras izquierda")
	#Femrus derecha
	pwm.set_pwm(FDT, 0, girar(delante_d))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(delante_i))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(delante_d))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(90))
	sleep(t)
	
	print("Bajar tarsos derecha, levantar izxquierda")
	#Tarsoso derecha
	pwm.set_pwm(TDT, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(down_d))
	sleep(t)
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(up_i))
	sleep(t)
	
	print("Avanzan los de derecha, los de izqueirda pa atras")
	#Femurs derecha
	pwm.set_pwm(FDT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(90))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(delante_i))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(delante_d))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(delante_i))
	sleep(t)
	
	print("Secuencia terminada")
	print("Reiniciando...")

def retroceder():		#Retroceder levantando 3 a la vez (ideal si spike puede levantar las patas)
	print("Vuelta izquierda: ")
	print("Levantar tarsos derecha, bajar izquierda")
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(down_i))
	sleep(t)
	#Tarsos derecha
	pwm.set_pwm(TDT, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(up_d))
	sleep(t)
	
	print("Delante femurs derecha, atras izquierda")
	#Femrus derecha
	pwm.set_pwm(FDT, 0, girar(detras_d))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(detras_i))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(detras_d))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(90))
	sleep(t)
	
	print("Bajar tarsos derecha, levantar izxquierda")
	#Tarsoso derecha
	pwm.set_pwm(TDT, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(down_d))
	sleep(t)
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(up_i))
	sleep(t)
	
	print("Avanzan los de derecha, los de izqueirda pa atras")
	#Femurs derecha
	pwm.set_pwm(FDT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(90))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(detras_i))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(detras_d))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(detras_i))
	sleep(t)
	
	print("Secuencia terminada")
	print("Reiniciando...")

def adelante():			#Avanzar moviendo una pata a la vez hacia delante y luego regresando todas para que se arrastre (ideal si spike no puede levantas las patas)
	for i in femur_I:
		pwm.set_pwm(i+1, 0, girar(up_i))
		sleep(t)
		pwm.set_pwm(i, 0, girar(delante_i))
		sleep(t)
		pwm.set_pwm(i+1, 0, girar(down_i))
		sleep(t)
		pwm.set_pwm(i+7, 0, girar(up_d))
		sleep(t)
		pwm.set_pwm(i+6, 0, girar(delante_d))
		sleep(t)
		pwm.set_pwm(i+7, 0, girar(down_d))
		sleep(t)
		
	for i in femur_D:
		pwm.set_pwm(i, 0, girar(detras_d))
		sleep(t)
	for i in femur_I:
		pwm.set_pwm(i, 0, girar(detras_i))
		sleep(t)

def atras():			#Retroceder moviendo una pata a la vez hacia delante y luego regresando todas para que se arrastre (ideal si spike no puede levantas las patas)
	for i in femur_I:
		pwm.set_pwm(i+1, 0, girar(up_i))
		sleep(t)
		pwm.set_pwm(i, 0, girar(detras_i))
		sleep(t)
		pwm.set_pwm(i+1, 0, girar(down_i))
		sleep(t)
		pwm.set_pwm(i+7, 0, girar(up_d))
		sleep(t)
		pwm.set_pwm(i+6, 0, girar(detras_d))
		sleep(t)
		pwm.set_pwm(i+7, 0, girar(down_d))
		sleep(t)
		
	for i in femur_D:
		pwm.set_pwm(i, 0, girar(delante_d))
		sleep(t)
	for i in femur_I:
		pwm.set_pwm(i, 0, girar(delante_i))
		sleep(t)

def tarsos90():			#Poner los tarsos en 90 grados
	for i in tarsos:
		print("90")
		pwm.set_pwm(i, 0, girar(90))
		sleep(t)

def femurs90():			#Poner los femurs en 90 grados
	for i in femurs:
		print("femurs90")
		pwm.set_pwm(i, 0, girar(90))
		sleep(t)

def iniciales():		#Bajar tarsos en posicion para caminar y poner los femurs en 90 grados
		print("Condiciones iniciales:")
		for i in tarso_I:
			pwm.set_pwm(i, 0, girar(down_i))
			sleep(t)
		for d in tarso_D:
			pwm.set_pwm(d, 0, girar(down_d))
			sleep(t)
		femurs90()
		
def izquierda():		#Girar a la izquierda
	print("Vuelta izquierda: ")
	print("Levantar tarsos derecha, bajar izquierda")
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(down_i))
	sleep(t)
	#Tarsos derecha
	pwm.set_pwm(TDT, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(up_d))
	sleep(t_espera)
	
	print("Delante femurs derecha, atras izquierda")
	#Femrus derecha
	pwm.set_pwm(FDT, 0, girar(delante_d))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(detras_i))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(delante_d))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(90))
	sleep(t_espera)
	
	print("Bajar tarsos derecha, levantar izxquierda")
	#Tarsoso derecha
	pwm.set_pwm(TDT, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(down_d))
	sleep(t)
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(up_i))
	sleep(t_espera)
	
	print("Avanzan los de derecha, los de izqueirda pa atras")
	#Femurs derecha
	pwm.set_pwm(FDT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(90))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(detras_i))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(delante_d))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(detras_i))
	sleep(t_espera)
	
	print("Secuencia terminada")
	print("Reiniciando...")

def derecha():			#Girar a la derecha
	print("Vuelta derecha: ")
	print("Levantar tarsos derecha, bajar izquierda")
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(down_i))
	sleep(t)
	#Tarsos derecha
	pwm.set_pwm(TDT, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(up_d))
	sleep(t_espera)
	
	print("Detraws femurs derecha, delante izquierda")
	#Femrus derecha
	pwm.set_pwm(FDT, 0, girar(detras_d))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(delante_i))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(detras_d))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(90))
	sleep(t_espera)
	
	print("Bajar tarsos derecha, levantar izxquierda")
	#Tarsoso derecha
	pwm.set_pwm(TDT, 0, girar(down_d))
	sleep(t)
	pwm.set_pwm(TIM, 0, girar(down_i))
	sleep(t)
	pwm.set_pwm(TDB, 0, girar(down_d))
	sleep(t)
	#Tarsos izquierda
	pwm.set_pwm(TIT, 0, girar(up_i))
	sleep(t)
	pwm.set_pwm(TDM, 0, girar(up_d))
	sleep(t)
	pwm.set_pwm(TIB, 0, girar(up_i))
	sleep(t_espera)
	
	print("Avanzan los de izquierda, los de delante pa atras")
	#Femurs derecha
	pwm.set_pwm(FDT, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FIM, 0, girar(90))
	sleep(t)
	pwm.set_pwm(FDB, 0, girar(90))
	sleep(t)
	#Femurs izquierda
	pwm.set_pwm(FIT, 0, girar(delante_i))
	sleep(t)
	pwm.set_pwm(FDM, 0, girar(detras_d))
	sleep(t)
	pwm.set_pwm(FIB, 0, girar(delante_i))
	sleep(t_espera)
	
	print("Secuencia terminada")
	print("Reiniciando...")

def a_mimir():			#Levantar los tarsos y dejar femurs en 90 grados
	for i in tarso_I:
		pwm.set_pwm(i, 0, girar(25))
		sleep(t)
	for i in tarso_D:
		pwm.set_pwm(i, 0, girar(155))
		sleep(t)
	
	femurs90()						
	 
def iniciar():			#Iniciar al sensor
	#Aample rate
	bus.write_byte_data(add, sample_rate , 7)
	
	#power management
	bus.write_byte_data(add, power, 1)
	
	#Configuration register
	bus.write_byte_data(add, conf, 0)
	
	#Gyro configuration register
	bus.write_byte_data(add, gyro_conf, 24)
	
	#Interrupt enable register
	bus.write_byte_data(add, interrup, 1)

def leer_datos(addr):	#Leer datos del sensor (addr = direccion hexadecimal de la orientación a leer)
	#Leer datos
        high = bus.read_byte_data(add, addr)
        low = bus.read_byte_data(add, addr+1)
    
        #Combinarlos 
        valor = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(valor > 32768):
                valor = valor - 65536
        return valor/16384.0
	
def iniciarBT():		#Realizar acción inicial usando bluedot
	print("Iniciar")
	iniciales()
	
def descansarBT():		#Realizar acción descabsar usando bluedot
	print("Descansar")
	a_mimir()
	
def adelanteBT():		#Realizar acción adelante usando bluedot
    print("adelante")
    #adelante()		#Descomentar si spike no levanta patas, comentar si spike levanta patas
    avanzar()		#Descomentar si spike levanta patas, comentar si spike no levanta patas

def atrasBT():			#Realizar acción atras usando bluedot
    print("atras")	
    #eatras()		#Descomentar si spike no levanta patas, comentar si spike levanta patas
    retroceder()	#Descomentar si spike levanta patas, comentar si spike no levanta patas

def izquierdaBT():		#Realizar acción girar izquierda usando bluedot
    print("izquierda")
    izquierda()

def derechaBT():		#Realizar acción girar derecha usando bluedot
    print("derecha")
    derecha()

"""------------------------------------------------------------------------------------------------------------------""" 
bus = smbus.SMBus(1) 	#Iniciar bus de datos para dispositivos i2c

"""Iniciar Bluetooth usando BlueDot"""
bd = BlueDot(cols=3, rows=5)	#Iniciar distribucion de botones en bluedot	
bd.color = "gray"				#Color de los botones
bd.square = True				#Botones con forma de cuadrado

#Poner invisibles a los botones que no queremos usar
bd[0,0].visible = False
bd[2,0].visible = False
bd[0,1].visible = False
bd[1,1].visible = False
bd[2,1].visible = False
bd[0,2].visible = False
bd[2,2].visible = False
bd[0,4].visible = False
bd[2,4].visible = False

#Poner verde al boton de inicio, rojo el boton de descanso
bd[1,0].color = "green"
bd[1,3].color = "red"

iniciar()		#Iniciar sensor
print ("Leyendo:")		

"""La estructura |try:	except:| nos ayuda a que el codigo siempre haga lo que esté en el try a menos que se haga la acción del except"""

try:
	#Especificar la acción que realizará [x,y] botón de BlueDot al ser precionado:
	bd[1,2].when_pressed = adelanteBT
	bd[1,4].when_pressed = atrasBT
	bd[0,3].when_pressed = izquierdaBT
	bd[2,3].when_pressed = derechaBT
	bd[1,0].when_pressed = iniciarBT
	bd[1,3].when_pressed = descansarBT

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	#Descomentar todas estas lineas en caso de querer hacer un bucle de alguno de los movimiento (también se deberá comentar o descomentar el movimiento deseado)
	"""
	while True:	
		#Read Gyroscope raw value
		#x = leer_datos(x_dir)
		#x = (-0.9956157522543754)*x + (0.7281501247343715)
		#print(f"X: {x}g")
		#print("90")
		#pwm.set_pwm(0, 0, girar(90))
		#sleep(1)
		
		#iniciales()
		#a_mimir()
		#izquierda()		
		#derecha()
		#tarsos90()
		#femurs90()
		
		#adelante()
		#atras()
	"""
	#-----------------------------------------------------------------------------------------------------------------------------------------------------------
	
except KeyboardInterrupt:	#Esta interrupción sucede cuando en la terminal de la raspberry realizamos el comando ctrl+c para interrumpir el código
	"""Lineas MUY importantes, no quitar por nada: """
	for i in range(15):			#For para hacer que los servos dejen de moverse (en caso de que se encuentren en algun movimiento)
		pwm.set_pwm(i, 0, 0)

	bd.stop()	#detener el uso del canal de Bluetooth (En caso de olvidar esta linea existe la posibilidad de que el canal no se cierre por si mismo y el Bluetooth de la ras quede inutl)			

pause()	#Pausar uso del BlueDot
