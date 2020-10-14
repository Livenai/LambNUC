"""
Este script realiza un ligero estudio estadistico sobre los datos del dataset de la fase 2 (pesos).
Para ello necesita leer los archivos .json del dataset.
"""

import glob, json, os
import numpy as np


UMBRAL_MAX_PESO = 35.0

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


num_images = 0
all_data = []


try:
	# obtencion de datos de cada JSON
	for json_number, json_name in enumerate(glob.glob(os.path.join(os.path.join(parent_folder, "savings"), '*.json'))):
		# abrimos el json
		f = open(json_name)
		j = json.load(f)

		# por cada entrada
		i = 0
		for key in j:
			num_images = num_images + 1
			i += 1
			all_data.append(j[key])
		print("Numero del Json: " + str(json_number))
		print("Imagenes en el Json: " + str(i), end='\n\n')
except:
	print("Error al leer los .json (quizas no haya imagenes aun)")
	exit("-- No hay estadisticas --")

if len(all_data) == 0:
	exit("No hay imagenes ni carpeta savings")

print("Imagenes Totales:" + " " + str(num_images) , end='\n\n')


# organizamos los datos
lista_pesos_validos = []
lista_pesos_no_validos = []
num_pesos_cero = 0
for dato in all_data:
	peso = dato["weight"]
	if peso < 1:
		num_pesos_cero += 1
	elif peso > UMBRAL_MAX_PESO:
		lista_pesos_no_validos.append(peso)
	else:
		lista_pesos_validos.append(peso)

# realizamos el estudio de los datos
lista_pesos_validos = np.array(lista_pesos_validos)
lista_pesos_no_validos = np.array(lista_pesos_no_validos)

media_de_pesos_validos = lista_pesos_validos.mean()
desviacion_de_pesos_validos = lista_pesos_validos.std()
varianza_de_pesos_validos = lista_pesos_validos.var()

p_pesos_validos = (lista_pesos_validos.size / num_images) * 100
p_pesos_no_validos = (lista_pesos_no_validos.size / num_images) * 100
p_pesos_cero = (num_pesos_cero / num_images) * 100

if lista_pesos_no_validos.size > 0:
    peso_maximo = np.max(lista_pesos_no_validos)
else:
    peso_maximo = np.max(lista_pesos_validos)

# mostramos los resultados
print("=================  " + "Resultado del estudio" + "  =================\n")
print("Imagenes totales: " + str(num_images) )
print("Peso maximo permitido: " + str(UMBRAL_MAX_PESO) + " Kg\n")

print("Imagenes con peso valido: " + str(lista_pesos_validos.size) + " (" + str(round(p_pesos_validos,2)) + "%)")
print("Media de pesos validos: " + str(round(media_de_pesos_validos,2)) + " Kg")
print("Desviacion tipica: " + str(round(desviacion_de_pesos_validos,2)) + " Kg")
print("Varianza: " + str(round(varianza_de_pesos_validos,2)) + "\n")

print("Imagenes con peso invalido (mayor al maximo peso permitido): " + str(lista_pesos_no_validos.size) + " (" + str(round(p_pesos_no_validos,2)) + "%)")
print("Imagenes con peso cero: " + str(num_pesos_cero) + " (" + str(round(p_pesos_cero,2)) + "%)\n")

print("Mayor peso encontrado: " + str(peso_maximo) + " Kg\n")


