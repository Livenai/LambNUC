#!/usr/bin/python3
# -*- coding: utf-8 -*-                                                                                                                                                                                                                     $import telepot
import os
import glob

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


#obtenemos todos los archivos a subir
path = os.path.join(parent_folder, "savings")
files = [f for f in glob.glob(os.path.join(path, "**" , "*.*"), recursive=True)]

for f in files:
	print(f)
