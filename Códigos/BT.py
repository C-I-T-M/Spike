#Librerias externas:
from bluedot import BlueDot;		"""Información: https://bluedot.readthedocs.io/en/latest/gettingstarted.html"""

#Librerias internas:
from signal import pause;			"""Información: https://docs.python.org/3/library/signal.html"""

"""------------------------------------------------------------------------------------------------------------------"""
"""Funciones: """
def iniciarBT():		#Realizar acción inicial usando bluedot
	print("Iniciar")
	
def descansarBT():		#Realizar acción descabsar usando bluedot
	print("Descansar")
	
def adelanteBT():		#Realizar acción adelante usando bluedot
    print("adelante")
    
def atrasBT():			#Realizar acción atras usando bluedot
    print("atras")	
    
def izquierdaBT():		#Realizar acción girar izquierda usando bluedot
    print("izquierda")

def derechaBT():		#Realizar acción girar derecha usando bluedot
    print("derecha")

"""------------------------------------------------------------------------------------------------------------------""" 

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

try:
	#Especificar la acción que realizará [x,y] botón de BlueDot al ser presionado:
	bd[1,2].when_pressed = adelanteBT
	bd[1,4].when_pressed = atrasBT
	bd[0,3].when_pressed = izquierdaBT
	bd[2,3].when_pressed = derechaBT
	bd[1,0].when_pressed = iniciarBT
	bd[1,3].when_pressed = descansarBT
      
except KeyboardInterrupt:
	print("Interrupcion")
	bd.stop()	#detener el uso del canal de Bluetooth (En caso de olvidar esta linea existe la posibilidad de que el canal no se cierre por si mismo y el Bluetooth de la ras quede inutl)			

pause()	#Pausar uso del BlueDot