#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json, os, glob
from telebot_send import send_msg

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


#obtenemos todos los archivos json
path = os.path.join(parent_folder, "savings")
files = [f for f in glob.glob(os.path.join(path, "**" , "*.json"), recursive=True)]




lamb = 0
wrong = 0
empty = 0
zero = 0

for names in files:
        file = open(names, "r")
        js = json.load(file)
        for k in js:
                if js[k]["label"] == "lamb":
                        lamb += 1
                if js[k]["label"] == "wrong":
                        wrong += 1
                if js[k]["label"] == "empty":
                        empty += 1
                if int(js[k]["weight"]) == 0:
                        zero += 1
msg = "lamb: " + str(lamb) + "\n" + "wrong: " + str(wrong) + "\n" + "empty: " + str(empty) + "\n" + "zero: " + str(zero) + "\n"
print(msg)

send_msg("Recuento en savings:\n\n" + msg)
