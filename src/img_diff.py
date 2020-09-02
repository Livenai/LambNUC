import glob, cv2
import numpy as np

def diff_percent_between_two_img(img_a, img_b):
	# crop de la region de interes para las imagenes
	x = 0
	y = 80
	h = 306
	w = 640
	#img = img[y:y + h, x:x + w]
	
	
	# recortamos la region de interes
	img_a = img_a[y:y + h, x:x + w]
	img_b = img_b[y:y + h, x:x + w]


	# las transformamos a uint8
	img_a = cv2.convertScaleAbs(img_a, alpha=(255.0/65535.0))
	img_b = cv2.convertScaleAbs(img_b, alpha=(255.0/65535.0))


	# obtenemos la matriz diferencia absoluta
	img_sub = np.absolute(img_a - img_b)

	# declaramos el maximo valor del pixel uint8
	MAX = int('11111111', 2)

	# normalizamos la matriz de diferencias absolutas
	img_diff_p = np.true_divide(img_sub, np.full(img_sub.shape, MAX, img_sub.dtype))

	# obtenemos elporcentaje de diferencia entre las dos imagenes 
	#(una matriz de diferencias absolutas blanca representaria dos imagenes 100% diferentes)
	img_diff_number = img_diff_p.sum() / img_diff_p.size


	# DEPURACION
	# print("diff int value: " + str(round(img_diff_number*100, 2)) + " %")
	# cv2.imshow('A',img_a*30)
	# cv2.imshow('B',img_b*30)
	# cv2.imshow('DIFF',img_diff_p)
	# cv2.waitKey(0)
	
	
	
	return img_diff_number

