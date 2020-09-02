#!/usr/bin/python3
# -*- coding: utf-8 -*-                                                                                                                                                                                                                     $import telepot
from mega import Mega
import os
import glob
from telebot_send import send_msg

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def upload_all():
	#obtenemos email y pass del archivo
        cf = open(os.path.join(parent_folder, "etc", "cloud_credentials"), 'r')
        email = cf.readline().replace("\n", "")
        password  = cf.readline().replace("\n", "")
        cf.close()
        print("Cloud credentials obtained succesfully.")
        send_msg("Cloud credentials obtained succesfully.")
        print("email: \"" + email + "\"   pass: \"" + password + "\"")



        #iniciamos sesion en la nube
        print("Logging in...")
        mega = Mega()
        M = mega.login(email, password)
        print("Logged in succesfully.")
        send_msg("Logged in succesfully.")

        #usamos la nube
        space = M.get_storage_space(giga=True)
        print("Space ->    Used: " + str(space["used"]) + "   Avaiable: " + str(space["total"]))
        send_msg("Space ->    Used: " + str(space["used"]) + "   Avaiable: " + str(space["total"]))

        #obtenemos todos los archivos a subir
        path = os.path.join(parent_folder, "savings")
        files = [f for f in glob.glob(os.path.join(path, "**" , "*.*"), recursive=True)]


        #subimos los archivos a la nube
        i = 0
        k = 0
        max_k = 1000
        while i < len(files):
                try:
                        #subimos el archivo con la ruta en el nombre (se usa / como separacion entre folders)
                        M.upload(files[i], dest_filename=files[i])
                        i += 1
                        k += 1
                        print("Archivo " + str(files[i]) + " (" + str(i) + ") subido correctamente.")
                        if k >= 1000:
                            send_msg(str(i) + " archivos subidos.")
                            k = 0
                except:
                        send_msg(":exclamation_mark: Error al subir el archivo " + str(i) + " a la nube.\n" + str(files[i]) + "\nReintentando...")

        print("num_files:  " + str(i))

def upload():
	#obtenemos email y pass del archivo
	cf = open(os.path.join(parent_folder, "etc", "cloud_credentials"), 'r')
	email = cf.readline().replace("\n", "")
	password  = cf.readline().replace("\n", "")
	cf.close()
	print("Cloud credentials obtained succesfully.")
	print("email: \"" + email + "\"   pass: \"" + password + "\"")



	#iniciamos sesion en la nube
	print("Logging in...")
	mega = Mega()
	M = mega.login(email, password)
	print("Logged in succesfully.")

	#usamos la nube
	space = M.get_storage_space(giga=True)
	print("Space ->    Used: " + str(space["used"]) + "   Avaiable: " + str(space["total"]))


	#obtenemos todos los archivos a subir
	path = os.path.join(parent_folder, "savings")
	files = [f for f in glob.glob(os.path.join(path, "**" , "*.*"), recursive=True)]


	#subimos los archivos a la nube
	i = 0
	k = 0
	msg_k = 100
	while i < len(files):
		try:
			#creamos el folder
			M_path = files[i][files[i].find("savings"):files[i].rfind("/")]
			M.create_folder(M_path)
			print("M_path: " + str(M_path))

			#subimos al folder
			folder = M.find(M_path)
			print("folder: " + str(folder))
			M.upload(files[i], folder[0])
			i += 1
		except:
			send_msg(":exclamation_mark: Error al subir el archivo " + str(i) + " a la nube.\nReintentando...")

	print("num_files:  " + str(i))


def upload_files_to_cloud():
	try:
		upload()
		#send succes telegram msg
		send_msg("Todas las Imagenes han sido subidas a la nube con exito :thumbs_up:")
	except Exception as e:
		#send fail telegram msg
		send_msg("Error al subir las imagenes a la nube :cross_mark:\n==================================\n" + repr(e))

upload_all()
#upload_files_to_cloud()
#upload()
