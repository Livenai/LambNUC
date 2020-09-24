"""
Este script realiza un ligero estudio estadistico sobre los datos del dataset de la fase 2 (pesos).
Para ello necesita leer los archivos .json del dataset.
"""

import glob, json, os
from colored import fg, attr
import numpy as np

B = fg(15)
C = fg(45)

UMBRAL_MAX_PESO = 35.0

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


num_images = 0
all_data = []

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
	print("Numero del Json: " + C + str(json_number) + B)
	print("Imagenes en el Json: " + C + str(i) + B, end='\n\n')

print(attr(4) + "Imagenes Totales:" + attr(0) + " " + C + str(num_images) + B, end='\n\n')


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
print("=================  " + C + "Resultado del estudio" + B + "  =================\n")
print("Imagenes totales: " + C + str(num_images) + B)
print("Peso maximo permitido: " + fg(2) + str(UMBRAL_MAX_PESO) + B + " Kg\n")

print("Imagenes con peso valido: " + C + str(lista_pesos_validos.size) + B + " (" + fg(51) + str(round(p_pesos_validos,2)) + B + "%)")
print("Media de pesos validos: " + C + str(round(media_de_pesos_validos,2)) + B + " Kg")
print("Desviacion tipica: " + C + str(round(desviacion_de_pesos_validos,2)) + B + " Kg")
print("Varianza: " + C + str(round(varianza_de_pesos_validos,2)) + B + "\n")

print("Imagenes con peso invalido (mayor al maximo peso permitido): " + fg(208) + str(lista_pesos_no_validos.size) + B + " (" + fg(209) + str(round(p_pesos_no_validos,2)) + B + "%)")
print("Imagenes con peso cero: " + fg(246) + str(num_pesos_cero) + B + " (" + fg(249) + str(round(p_pesos_cero,2)) + B + "%)\n")

print("Mayor peso encontrado: " + fg(202) + str(peso_maximo) + B + " Kg\n")


